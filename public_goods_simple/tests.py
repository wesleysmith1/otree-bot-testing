from otree.api import Currency as cu, currency_range, expect
from . import *
from otree.api import Bot



class PlayerBot(Bot):
    def play_round(self):
        yield Contribute, dict(contribution=cu(1))
        yield Results
