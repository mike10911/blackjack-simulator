# Michael Mundia
# CHS Computer Programming
# Pitt Project 2 Part 5
# 4/7/20, Mr.Costantino

import random


#All "card" variables are now replaced with the card variable from string_of_card to incorperate both the suit and value of card
def play_hand(name, bet):

    #deals out cards to player and dealer randomly using randint
    #the play hand now takes on two varibles. This takes on the new custom bet of the player and the name of player
    #now the deck is incorperated into the play hand function. THIS ALLOW THE SUITS TO APPEAR. the deck of cards is also randomized

    deck = new_deck()
    shuffle_deck(deck)
    player_hand = []
    dealer_hand = []
    player_stay = False
    dealer_stay = False
    dealer_hand.append(deck.pop(0))
    print(f"\nDealer's Hand:  {string_of_hand(dealer_hand)}.")
    print(f"Value: {value_of_hand(dealer_hand)}")
    player_hand.append(deck.pop(0))
    player_hand.append(deck.pop(0))
    print(f"{name} Hand:  {string_of_hand(player_hand)}.")
    print(f"Value: {value_of_hand(player_hand)}.")

    while True:
        print("\n")
        # if statements used to determine bust, push, wins
        # also used for the 25 dollar bet
        # now 25 dollar bet is replaced with a custom bet from the player

        player_value = value_of_hand(player_hand)
        dealer_value = value_of_hand(dealer_hand)

        if (player_value == dealer_value and dealer_value == 21):
            print("Push.")
            return 0

        if (player_value > 21):
            print(f"{name} busts.")
            return -bet

        elif (dealer_value > 21):
            print("Dealer busts.")
            return bet

        elif (dealer_value == 21):
            print("Dealer wins!")
            return -bet

        elif (player_value == 21):
            print(f"{name} wins!")
            return bet

        elif (player_stay and dealer_stay):
            if player_value > dealer_value:
                print(f"{name} wins.")
                return bet

            elif player_value == dealer_value:
                print("Push.")
                return 0

            else:
                print("Dealer wins.")
                return -bet

        #for if player hits or stays
        if not player_stay:
            move = None
            while move not in ["h", "s", "hit", "stay"]:
                move = input("Move? (hit/stay)\n").strip().lower()

            if move in ["s", "stay"]:
                player_stay = True

        if dealer_value >= 17:
            dealer_stay = True

        if not dealer_stay and player_stay:
            dealer_hand.append(deck.pop(0))

        print(f"\nDealer's Hand:  {string_of_hand(dealer_hand)}.")
        print(f"Value: {value_of_hand(dealer_hand)}.")

        if not player_stay:
            player_hand.append(deck.pop(0))

        print(f"{name} Hand  {string_of_hand(player_hand)}.")
        print(f"Value: {value_of_hand(player_hand)}.")


#input vaildation takes on the bet and your money and determines if you have enough money or if the bet is a valid input
#tried to used try and except but it didn't get me anywhere so I used if-else statements
def input_bet(bet, money):
    while True:

        new_bet = input(
            f"Bet? (0 to quit, Enter to stay at {bet})\n").strip().replace(
                "$", "")

        if new_bet.isdecimal():
            new_bet = int(new_bet)

            if new_bet <= money:
                return new_bet

            else:
                print(f"You only have ${money}.\nYou can't bet ${new_bet}.")

        elif len(new_bet) == 0:
            if bet <= money:
                return bet
            else:
                print(f"You only have ${money}.\nYou can't bet ${bet}.")
        else:
            print("Invalid input.")


#the save function allow the user to save the game which they have play
#takes on variables name and money
def save(name, money):
    try:
        f = open("blackjack.save", 'w')
        f.write(name + "\n")
        f.write(str(money))
        f.close()
    except:
        print("Data could not be saved.")


#Allows you to reload your game
def restore():
    try:
        f = open("blackjack.save", 'r')
        lines = f.readlines()
        f.close()
        name = lines[0]
        money = int(lines[1])
        return name.strip(), money
    except:
        return '', -1


#This function allows each card to have one of 4 suits
#loops through values and gives suits
def new_deck():
    output = []
    suits = ['\u2660', '\u2661', '\u2662', '\u2663']
    for suit in suits:
        for rank in range(1, 14):
            output.append((rank, suit))
    return output


#randomly shuffles
def shuffle_deck(deck):
    random.shuffle(deck)


#This is for the face card values and the Ace
def value_of_card(card):
    if card[0] > 9:
        return 10
    elif card[0] > 1:
        return card[0]
    else:
        return 11


#For face card value form number to letter
def string_of_card(card):
    letter = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}
    value = card[0]
    suit = card[1]
    if value > 10 or value == 1:
        return f"{letter[value]}{suit}"
    else:
        return f"{value}{suit}"


def string_of_hand(hand):
    return " ".join(string_of_card(card) for card in hand)


def value_of_hand(hand):
    #aces now must have its own variable to change since aces have two values
    value = 0
    aces = 0

    #Ace calculation #used my own
    for card in hand:
        if value_of_card(card) == 11:
            aces += 1
        else:
            value += value_of_card(card)
    if aces > 0:
        if (value + 11 + aces - 1) <= 21:
            return value + 11 + aces - 1
    return value + aces


def main():
    #now in the begining you can restore your old data
    #staring values are now incorperated in the restore if statements
    data = restore()
    load = False

    if not data[1] <= 0:
        resume = input(f"Resume saved game {data[0]}?\n").lower()
        if resume in ['y', 'yes', 'yeah']:
            load = True

    if load:
        money = data[1]
        name = data[0]
    else:
        money = 1000
        name = input("Player name: ").capitalize()

    bet = 0
    print(f"{name} has ${money}.")

    while (money > 0):
        bet = input_bet(bet, money)
        if bet == 0:
            break

        money += play_hand(name, bet)
        print(f"\n{name} has ${money}.")

    save(name, money)
    input("\nThanks for playing.\n")


if __name__ == '__main__':
    main()
