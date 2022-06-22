from otree.api import Currency as cu, currency_range, SubmissionMustFail, expect
from . import *
from otree.api import Bot



class PlayerBot(Bot):

    cases = ['basic', 'p1_wins', 'all_0', 'all_max']

    def play_round(self):
        case = self.case

        # Introduction
        yield Introduction

        if case == 'basic':
            for invalid_bid in [-1, 11]:
                yield SubmissionMustFail(Bid, dict(bid_amount=invalid_bid))
        if case == 'p1_wins':
            if self.player.id_in_group == 1:
                bid_amount = 2
            else:
                bid_amount = 1
        elif case == 'all_0':
            bid_amount = 0
        else:  # case == 'all_max':
            bid_amount = Constants.max_allowable_bid
        yield Bid, dict(bid_amount=bid_amount)

        if case == 'p1_wins':
            if self.player.id_in_group == 1:
                expect('You won the auction', 'in', self.html)
            else:
                expect('You did not win', 'in', self.html)

        if self.player.id_in_group == 1:
            num_winners = sum([1 for p in self.group.get_players() if p.is_winner])
            expect(num_winners, 1)

        for field in [
            self.player.bid_amount,
            self.player.payoff,
            self.player.item_value_estimate,
            self.player.is_winner,
        ]:
            expect(field, '!=', None)

        yield Results
