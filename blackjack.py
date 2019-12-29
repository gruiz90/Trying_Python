"""
Blackjack
"""
# from IPython.display import clear_output
import random
import math

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
		 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7,
		  'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10,
		  'King': 10, 'Ace': 11}

print_ranks = {'Two': '2', 'Three': '3', 'Four': '4', 'Five': '5',
						   'Six': '6', 'Seven': '7', 'Eight': '8', 'Nine': '9',
						   'Ten': '10', 'Jack': 'J', 'Queen': 'Q', 'King': 'K', 'Ace': 'A'}
print_suits = {'Hearts': '♡', 'Diamonds': '♢', 'Spades': '♠', 'Clubs': '♣'}


class Card:
	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank
		self.value = values[self.rank]

	def __str__(self):
		return print_ranks[self.rank] + print_suits[self.suit]


class Deck:
	def __init__(self, mixed=True):
		self.cards = []
		for suit in suits:
			for rank in ranks:
				card = Card(suit, rank)
				self.cards.append(card)
		if mixed:
			self.shuffle()

	def __str__(self):
		result = '| '
		for card in self.cards:
			result += card.__str__() + ' | '
		return result + '\n'

	def shuffle(self):
		random.shuffle(self.cards)


class Hand:
	def __init__(self):
		self.cards = []
		self.value = 0
		self.aces = 0
		self.blackjack = False

	def take_card(self, card):
		self.cards.append(card)
		self.value += card.value

		if card.rank == 'Ace':
			self.aces += 1

		if self.value > 21 and self.aces > 0:
			self.aces -= 1
			self.value -= 10

		if self.value == 21:
			self.blackjack = True


class Hand_Player(Hand):
	def __init__(self, bet):
		Hand.__init__(self)
		self.bet = bet
		self.double_down = False
		self.stand = False

	def __str__(self):
		if self.cards:
			hand_str = '| '
			for card in self.cards:
				hand_str += card.__str__() + ' | '
			hand_str += 'V: ' + str(self.value) + \
				' B: $' + str(self.bet) + ' S: '
			if self.stand:
				hand_str += 'Y'
				if self.double_down:
					hand_str += ' (DD)'
			else:
				hand_str += 'N'
		return hand_str + '\n'

	def take_card(self, card, double_down=False):
		Hand.take_card(self, card)

		if double_down:
			self.double_down = True
			self.stand = True
			self.bet *= 2


class Hand_Dealer(Hand):
	def __init__(self):
		Hand.__init__(self)
		self.show = False

	def __str__(self):
		hand_str = ''
		if self.cards:
			hand_str = '| '
			if not self.show:
				hand_str += self.cards[0].__str__() + ' | X | V: ?'
			else:
				for card in self.cards:
					hand_str += card.__str__() + ' | '
				hand_str += 'V: ' + str(self.value)
		return hand_str

	def is_soft_17(self, soft_17):
		if soft_17 and self.aces > 0 and self.value in range(17, 21):
			return True
		return False


class Player:
	def __init__(self, num, chips=100):
		self.player_num = num
		self.chips = chips
		self.hands = []
		self.is_out = False

	def __str__(self):
		hands_str = ''
		for hand in self.hands:
			hands_str += hand.__str__()
		hands_str += '\nBank: $' + str(self.chips)
		return hands_str + '\n'

	def make_bet(self, pair_cards, bet=10):
		self.chips -= bet
		hand = Hand_Player(bet)
		hand.take_card(pair_cards[0])
		hand.take_card(pair_cards[1])
		self.hands.clear()
		self.hands.append(hand)

	def hit(self, hand_position, card):
		self.hands[hand_position].take_card(card)

	def stand(self, hand_position):
		self.hands[hand_position].stand = True

	def double_down(self, hand_position, card):
		self.chips -= self.hands[hand_position].bet
		self.hands[hand_position].take_card(card, True)

	def split(self, hand_position, pair_cards):
		self.chips -= self.hands[hand_position].bet

		first_hand = Hand_Player(self.hands[hand_position].bet)
		first_hand.take_card(self.hands[hand_position].cards[0])
		first_hand.take_card(pair_cards[0])
		self.hands[hand_position] = first_hand

		second_hand = Hand_Player(self.hands[hand_position].bet)
		second_hand.take_card(self.hands[hand_position].cards[1])
		second_hand.take_card(pair_cards[1])
		self.hands.append(second_hand)

	def payout_hand(self, hand_position, blackjack):
		bet = self.hands[hand_position].bet
		self.chips += bet * 2
		if blackjack:
			self.chips += 0.5 * bet
			return bet * 1.5
		return bet

	def return_bet(self, hand_position):
		bet = self.hands[hand_position].bet
		self.chips += bet

	def check_blackjack(self, hand_position):
		if self.hands[hand_position].value == 21:
			winnings = self.payout_hand(hand_position, True)
			print(
				f"\nBlackjack!!! Player {self.player_num} hand ({hand_position+1}) wins: {winnings}")
			return True
		return False

	def check_bust(self, hand_position):
		if self.hands[hand_position].value > 21:
			print(
				f"\nPlayer {self.player_num} hand ({hand_position+1}) busted! Bet lost: {self.hands[hand_position].bet}")
			return True
		return False

	def is_standing(self, hand_position):
		return self.hands[hand_position].stand

	def can_double(self, hand_position):
		if len(self.hands[hand_position].cards) > 2 or self.hands[hand_position].bet > self.chips:
			return False
		return True

	def can_split(self, hand_position):
		if len(self.hands[hand_position].cards) == 2 and\
				self.hands[hand_position].cards[0].rank == self.hands[hand_position].cards[1].rank and\
				self.hands[hand_position].bet <= self.chips:
			return True
		return False


class Dealer:
	def __init__(self, number_of_decks=1, soft_17=True):
		self.number_of_decks = number_of_decks
		self.soft_17 = soft_17
		self.shoe_ordered = []
		for _ in range(0, number_of_decks):
			deck = Deck(False)
			for card in deck.cards:
				self.shoe_ordered.append(card)
		self.shoe = self.shoe_ordered.copy()
		self.shuffle_shoe()
		self.hand = Hand_Dealer

	def __str__(self):
		dealer_str = str(self.hand) + ' S17: '
		if self.soft_17:
			dealer_str += 'Yes'
		else:
			dealer_str += 'No'
		# dealer_str += ' | Number of cards in shoe remaining: ' + str(len(self.shoe))
		return dealer_str + '\n'

	def shuffle_shoe(self):
		random.shuffle(self.shoe)

	def deal(self):
		return self.shoe.pop()

	def init_hand(self):
		self.hand = Hand_Dealer()
		self.hand.take_card(self.deal())
		self.hand.take_card(self.deal())

	def complete_hand(self):
		self.hand.show = True
		while True:
			if self.hand.blackjack or self.hand.value > 21 or\
					self.hand.value in range(17, 21) and not self.hand.is_soft_17(self.soft_17):
				break
			else:
				self.hand.take_card(self.deal())

	def check_reset_shoe(self):
		total_cards_shoe = self.number_of_decks * 52
		cards_remaining_shoe = len(self.shoe)
		# print(f"{total_cards_shoe} - {cards_remaining_shoe}")
		if cards_remaining_shoe < 0.25 * total_cards_shoe:
			self.shoe = self.shoe_ordered.copy()
			self.shuffle_shoe()


class Blackjack:
	def __init__(self, number_of_decks=1, soft_17=False, players_chips=[100]):
		self.dealer = Dealer(number_of_decks, soft_17)
		self.players = []
		player_num = 1
		# Max of 3 players I guess
		for player_chips in players_chips:
			self.players.append(Player(player_num, player_chips))
			player_num += 1
			if player_num == 4:
				break

	def start_game(self):
		keep_playing = True
		print('\n'*100)
		while keep_playing:
			# Ask player/s to place bet
			for player in self.players:
				if not player.is_out:
					while True:
						try:
							player_bet = int(
								input(f"\nPlayer {player.player_num} (${player.chips}) - Place your bet: \n"))
						except:
							print(
								"\nThe bet needs to be an integer number that not exceeds the current amount of chips for the player...\n")
						else:
							if player_bet > player.chips:
								print(
									f"\nThe bet cannot exceed the current amount of chips for the player: {player.chips}\n")
							elif player_bet < 1:
								print(f"\nThe bet cannot be less than $1\n")
							else:
								break
					player.make_bet(
						(self.dealer.deal(), self.dealer.deal()), player_bet)
			# Here the dealer needs to get his hand
			self.dealer.init_hand()

			# Show game state here for each player and ask for actions
			dealer_show_cards = []
			for player in self.players:
				if not player.is_out:
					player_hands_count = 1
					player_hand_position = 0
					while True:
						# Show dealer and player state
						print('\n'*100)
						print(self.dealer)
						print(player)

						take_action = False
						if player.check_blackjack(player_hand_position) or\
								player.check_bust(player_hand_position):
							input("\nHand completed! Press enter to continue...\n")
							player_hand_position += 1
						elif player.is_standing(player_hand_position):
							dealer_show_cards.append(
								(player.player_num, player_hand_position))
							input(
								f"\nHand completed! Player {player.player_num} is standing hand ({player_hand_position+1}). Press enter to continue...\n")
							player_hand_position += 1
						else:
							take_action = True

						if player_hands_count == player_hand_position:
							# Then no more hands to check, need to break here
							break
						elif not take_action:
							continue

						actions_str = f"\nPlayer {player.player_num} Hand ({player_hand_position+1}) - Take action (Hit = H)(Stand = S)"
						can_double = False
						can_split = False
						if player.can_double(player_hand_position):
							can_double = True
							actions_str += "(Double Down = D)"
						if player.can_split(player_hand_position):
							can_split = True
							actions_str += "(Split = SP)"
						actions_str += ":\n"

						player_action = input(actions_str).upper()
						if player_action == "H":
							# Then deal another card for the player
							player.hit(player_hand_position, self.dealer.deal())
						elif player_action == "S":
							player.stand(player_hand_position)
						elif can_double and player_action == "D":
							player.double_down(
								player_hand_position, self.dealer.deal())
						elif can_split and player_action == "SP":
							player.split(player_hand_position,
										(self.dealer.deal(), self.dealer.deal()))
							player_hands_count += 1
						else:
							print("\nAction not recognized...\n")
							continue

			# Complete dealer hand if need to..
			if dealer_show_cards:
				input("\nDealers turn to complete hand. Press enter to continue...\n")
				self.dealer.complete_hand()

				for player_num, player_hand_position in dealer_show_cards:
					print('\n'*100)
					print("Dealer complete hand:\n")
					print(self.dealer)
					print(
						f"Player {player_num} complete hand ({player_hand_position+1}):\n")
					print(self.players[player_num -
									   1].hands[player_hand_position])

					if self.dealer.hand.blackjack:
						print("Dealer has a blackjack...")
						print(
							f"Player {player_num} loses bet: ${self.players[player_num-1].hands[player_hand_position].bet}")
					elif self.dealer.hand.value > 21:
						print("Dealer busted...")
						print(
							f"Player {player_num} wins bet: ${self.players[player_num-1].payout_hand(player_hand_position, False)}")
					elif self.dealer.hand.value == self.players[player_num-1].hands[player_hand_position].value:
						# In this case the bet is returned
						print("It's a Push...")
						print(
							f"Player {player_num} gets the bet back: ${self.players[player_num-1].hands[player_hand_position].bet}")
						self.players[player_num -
									 1].return_bet(player_hand_position)
					elif self.dealer.hand.value > self.players[player_num-1].hands[player_hand_position].value:
						print("Dealer wins...")
						print(
							f"Player {player_num} loses bet: ${self.players[player_num-1].hands[player_hand_position].bet}")
					else:
						print(
							f"Player {player_num} hand ({player_hand_position}) wins...")
						print(
							f"Player {player_num} wins bet: ${self.players[player_num-1].payout_hand(player_hand_position, False)}")
					print(
						f"Player {player_num} bank: ${self.players[player_num-1].chips}\n")

					input("Press enter to continue...\n")
			# Check for the players with no chips left
			no_chips_players = [
				player for player in self.players if player.chips == 0]
			for player in no_chips_players:
				if not player.is_out:
					print(f"Player {player.player_num} lost all chips!")
					player.is_out = True
			if len(no_chips_players) == len(self.players):
				# It's Game Over!
				input(
					"All the players are out. Game Over! Press any key to exit...\n")
				keep_playing = False
			else:
				# Continue playing?
				response = input("Round completed! Continue playing? (Y/N):\n").upper()
				while True:
					if response == "N":
						keep_playing = False
						break
					elif response == "Y":
						# Restart state if needed
						print('\n'*100)
						self.dealer.check_reset_shoe()
						break
					else:
						response = input("Action not recognized. Continue playing? (Y/N):\n").upper()


game = Blackjack(2, True, [100, 100])
game.start_game()
