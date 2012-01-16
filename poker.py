# -*- coding: utf-8 -*-

from random import shuffle, random, choice
from itertools import cycle

from checkers import Card, beats

class Player:
    def __init__(self):
        self.stake = 100

class g:
    player1, player2 = players = [Player() for i in range(2)]
    dealer_index = 0

def bet():
    max_bet = max([player.stake for player in g.players])
    range_ = range(len(g.players))
    first_bet_index = g.big_blind_index + 1
    if first_bet_index >= len(g.players):
        first_bet_index = 0
    while range_[0] != first_bet_index:
        range_.append(range_[0])
        del range_[0]
    for player_index in cycle(range_):
        if player_index == g.last_raised_index:
            break
        player = g.players[player_index]
        if g.min_bet == 0:
            choices = ['bet', 'check']
        else:
            choices = ['call', 'raise', 'fold']
        choice_ = choice(choices)
        min_bet = g.min_bet - player.last_bet
        print 'Player %i %s' % ((player_index + 1), choice_)
        if choice_ == 'fold':
            g.folded.append(player)
            if len(g.folded) == len(g.players) - 1:
                for player_ in g.players:
                    if player_ not in g.folded:
                        player_.stake += g.pot
                        return 'round over'
        elif choice_ == 'call':
            bet = min_bet - player.last_bet
        elif choice_ == 'check':
            bet = 0
        else:  # (bet or raise)
            bet = min_bet + round(random() * (player.stake - min_bet) * .1)
            g.last_raised_index = player_index
        if bet > max_bet:
            bet = max_bet
        g.min_bet = bet
        player.last_bet = bet
        player.stake -= bet
        g.pot += bet

def play_round():
    # Prepare for a new round.  Deal the flop.
    print 'New round'
    g.pot = 0
    g.folded = []
    g.min_bet = 0
    g.last_raised_index = None
    for player in g.players:
        player.last_bet = 0

    small_blind_index = dealer_index + 1
    if small_blind_index >= len(players):
        small_blind_index = 0
    big_blind_index = small_blind_index + 1
    if big_blind_index >= len(players):
        big_blind_index = 0
    players[small_blind_index].last_bet = small_blind
    players[big_blind_index].last_bet = big_blind

    deck = [Card(ch + suit) for ch in '23456789TJQKA' for suit in u'♥♦♣♠']
    shuffle(deck)
    hand1, hand2 = [deck.pop(), deck.pop()], [deck.pop(), deck.pop()]
    community = [deck.pop() for i in range(3)]

    # Place bets.  Deal a card.  End the round if all but one player folds.
    for i in range(2):
        result = bet()
        if result == 'round over':
            break
        community.append(deck.pop())
    if result == 'round over':
        for i, player in enumerate(g.players):
            if player in g.folded:
                print 'Player %i folded' % (i + 1)
    else:
        bet()

    # Print hand and winner.

    print hand1
    print community
    print hand2
    if len(g.folded) < len(g.players) - 1:
        p1_wins, hand_name = beats(hand1 + community, hand2 + community)
        print hand_name
        if p1_wins == 'tie':
            for player in g.players:
                player.stake += g.pot / len(g.players)
        elif p1_wins:
            print 'player 1 wins'
            g.player1.stake += g.pot
        else:
            print 'player 2 wins'
            g.player2.stake += g.pot
    print 'pot:', g.pot
    broke_indices = []
    for i, player in enumerate(g.players):
        print 'Player %i stake:' % (i + 1), player.stake
        if player.stake <= 0:
            broke_indices.append(i)
    if len(broke_indices) == len(g.players) - 1:
        for i in range(len(g.players)):
            if i not in broke_indices:
                print 'Player %i wins it all!' % i
                return True
    g.dealer_index += 1
    if g.dealer_index >= len(players):
        g.dealer_index = 0
    print

for i in range(100):
    if play_round():
        break