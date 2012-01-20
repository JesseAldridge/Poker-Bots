# -*- coding: utf-8 -*-


def straight_flush(cards):
    return flush(cards) and straight(sorted_hand(cards))
def four_of_a_kind(hand_vals):
    for num in hand_vals:
        if hand_vals.count(num) == 4:
            return num
def full_house(hand_vals):
    three_count, two_count = None, None
    for num in sorted(list(set(hand_vals))):
        if hand_vals.count(num) == 3 and not three_count:
            three_count = num
        elif hand_vals.count(num) == 2 and not two_count:
            two_count = num
    if three_count and two_count:
        return three_count, two_count
def flush(cards):
    card_suits = [card.suit for card in cards]
    flush_vals = [card.val for card in cards
                  if card_suits.count(card.suit) >= 5]
    if flush_vals:
        return max(flush_vals)
def straight(hand_vals):
    hand_vals = sorted(list(set(hand_vals)), reverse=True)
    for i in range(0, len(hand_vals) - 4):
        for j in range(i, i + 4):
            if hand_vals[j + 1] != hand_vals[j] - 1:
                break
        else:
            return hand_vals[i]
def three_of_a_kind(hand_vals):
    for val in hand_vals:
        if hand_vals.count(val) == 3:
            return val
def two_pairs(hand_vals):
    pairs = sorted([val for val in set(hand_vals) if hand_vals.count(val) == 2])
    if len(pairs) >= 2:
        return (pairs[-1], pairs[-2],
                max([val for val in hand_vals if val]))
def one_pair(hand_vals):
    for val in hand_vals:
        if hand_vals.count(val) == 2:
            return val

class Card:
    def __init__(self, s):
        self.val, self.suit = s[0], s[1]
    def __repr__(self):
        return (self.val + self.suit).encode('utf-8')

def vals(hand):  return [card.val for card in hand]
def suits(hand):  return [card.suit for card in hand]
def name_to_num(s):
    if s in '23456789': return int(s)
    return {'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}[s]

def sorted_hand(hand):
    return [name_to_num(s) for s in sorted(vals(hand), key=name_to_num,
                                           reverse=True)]

def is_higher(hand1, hand2):
    for num1, num2 in zip(hand1, hand2):
        if num1 > num2:  return True
        if num2 > num1:  return False
    return 'tie'

special_checkers = [straight_flush, four_of_a_kind, full_house,
                    flush, straight, three_of_a_kind, two_pairs, one_pair]

def beats(hand1, hand2):
    # Check for straight flush, full house, etc.  Check high on tie.
    for special_checker in special_checkers:
        cleaned1, cleaned2 = hand1, hand2
        if 'flush' not in special_checker.__name__:
            cleaned1, cleaned2 = [
                sorted_hand(hand) for hand in cleaned1, cleaned2]
        check1, check2 = [special_checker(hand) for hand in cleaned1, cleaned2]
        result = None
        if check1 > check2:  result = True
        elif check2 > check1:  result = False
        elif check1 and check2:  result = is_higher(cleaned1, cleaned2)
        if result is not None:
            return result, special_checker.__name__
    return is_higher(cleaned1, cleaned2), 'high card'

if __name__ == '__main__':
    def cards(card_strs):
        return [Card(unicode(s, 'utf-8')) for s in card_strs]

    for card_strs, checker in [
        (('J♥', 'T♣', '8♣', '9♣', '9♠', 'Q♠', 'A♠'), straight),
        (('9♣', '7♠', '8♦', '6♦', 'K♣', 'K♦', '8♠'), lambda v:  not straight(v)),
        (('6♦', '8♥', '3♣', '6♥', '6♣', 'A♦', 'J♠'), three_of_a_kind),
        (('Q♠', '3♦', '7♦', '4♠', '2♠', 'Q♦', '4♦'), one_pair),
    ]:
        assert checker(sorted_hand(cards(card_strs))), checker.__name__

    assert flush(cards(['J♠', '7♥', 'K♠', '9♠', '3♠', '5♠', 'T♦']))

    assert (beats(cards(['7♦', 'K♥', 'Q♥', 'Q♦', 'T♣', '9♦', '5♠']),
                  cards(['2♥', '6♥', 'Q♥', 'Q♦', 'T♣', '9♦', '5♠'])) ==
            (True, 'one_pair'))

    res = beats(cards(['3♣', '3♠', 'J♦', 'J♠', 'K♠', '6♣', '2♥',]),
                 cards(['3♣', '3♠', 'J♦', 'J♠', 'K♥', 'Q♦', '2♥',]))
    assert res == (False, 'two_pairs'), res
