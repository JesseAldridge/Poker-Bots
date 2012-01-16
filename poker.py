# -*- coding: utf-8 -*-

from random import shuffle, random, choice
from itertools import cycle

from checkers import Card, beats


class Player:
    def __init__(self):
        self.stake = 1000

class g:
    player0, player1 = players = [Player() for i in range(2)]
    dealer_index = 0
    small_blind_value = 10
    big_blind_value = 20


def bet(is_first_round=False):
    g.times_around = 0
    for player in g.players:
        player.last_bet = 0
    g.min_bet = 0

    if is_first_round:
        g.small_blind_index = inc_player(g.dealer_index)
        g.big_blind_index = inc_player(g.small_blind_index)
        place_bet(g.players[g.small_blind_index], g.small_blind_value)
        place_bet(g.players[g.big_blind_index], g.big_blind_value)
        g.last_raised_index = g.big_blind_index
        g.min_bet = g.big_blind_value

    max_bet = max([player.stake for player in g.players])
    range_ = range(len(g.players))
    first_bet_index = inc_player(g.big_blind_index)
    while range_[0] != first_bet_index:
        range_.append(range_[0])
        del range_[0]
    for player_index in cycle(range_):
        if player_index == g.last_raised_index:
            g.times_around += 1
            if g.times_around > 1:
                break
        player = g.players[player_index]
        if player_index == g.last_raised_index:
            choices = ['raise', 'check']
        elif g.min_bet == 0:
            choices = ['bet', 'check']
        else:
            choices = ['call', 'raise']
            if g.min_bet > 0:
                choices.append('fold')
        choice_ = choice(choices)
        min_bet = g.min_bet - player.last_bet
        print 'Player %i %s' % (player_index, choice_)
        if choice_ == 'fold':
            g.folded.append(player)
            if len(g.folded) == len(g.players) - 1:
                for player_ in g.players:
                    if player_ not in g.folded:
                        player_.stake += g.pot
                        return 'round over'
        elif choice_ == 'call':
            bet = min_bet
        elif choice_ == 'check':
            bet = 0
            if player_index == g.last_raised_index:
                break
        else:  # (bet or raise)
            bet = min_bet + round(random() * (player.stake - min_bet) * .1)
            g.last_raised_index = player_index
        if bet > max_bet:
            bet = max_bet
        print '  bet:', bet
        g.min_bet = bet
        player.last_bet = bet
        player.stake -= bet
        g.pot += bet

def inc_player(num):  return 0 if num + 1 >= len(g.players) else num + 1

def place_bet(player, val):
    player.last_bet = val
    g.pot += val
    player.stake -= val

def play_round():
    # Prepare for a new round.  Deal the flop.
    print 'New round'
    g.pot = 0
    g.folded = []

    print 'Player %i is dealer' % g.dealer_index
    deck = [Card(ch + suit) for ch in '23456789TJQKA' for suit in u'♥♦♣♠']
    shuffle(deck)
    hand1, hand2 = [deck.pop(), deck.pop()], [deck.pop(), deck.pop()]
    print hand1
    print hand2

    if bet(is_first_round=True) != 'round over':
        g.community = [deck.pop() for i in range(3)]
        print g.community

        # Deal a card.  Place bets.  End the round if all but one player folds.
        for i in range(2):
            g.community.append(deck.pop())
            result = bet()
            if result == 'round over':
                break
            print g.community
        if result == 'round over':
            for i, player in enumerate(g.players):
                if player in g.folded:
                    print 'Player %i folded' % i
        else:
            bet()

    # Print hand and winner.
    if len(g.folded) < len(g.players) - 1:
        p0_wins, hand_name = beats(hand1 + g.community, hand2 + g.community)
        print hand_name
        if p0_wins == 'tie':
            for player in g.players:
                player.stake += g.pot / len(g.players)
        elif p0_wins:
            print 'player 0 wins'
            g.player0.stake += g.pot
        else:
            print 'player 1 wins'
            g.player1.stake += g.pot
    print 'pot:', g.pot
    broke_indices = []
    for i, player in enumerate(g.players):
        print 'Player %i stake:' % i, player.stake
        if player.stake <= 0:
            broke_indices.append(i)
    if len(broke_indices) == len(g.players) - 1:
        for i in range(len(g.players)):
            if i not in broke_indices:
                print 'Player %i wins it all!' % i
                return True
    g.dealer_index += 1
    if g.dealer_index >= len(g.players):
        g.dealer_index = 0
    print

for i in range(100):
    if play_round():
        break