from otree.api import Currency as cu, currency_range, expect

from . import *
from otree.api import Bot



class PlayerBot(Bot):

    cases = [
        dict(age=19, gender='Male', crt_bat=100, crt_widget='abc', crt_lake=2, pass_demographics=True, pass_crt=False),
        dict(age=2, gender='Female', crt_bat=20, crt_widget=30, crt_lake=47, pass_demographics=False, pass_crt=True),
    ]

    def play_round(self):

        case = self.case
        print(case)

        if case['pass_demographics']:
            yield Demographics, dict(age=case['age'], gender=case['gender'])
        else:
            yield SubmissionMustFail(Demographics, dict(age=case['age'], gender=case['gender']))
            yield Demographics, dict(age=30, gender='Male')

        expect('Please answer the following questions', 'in', self.html)

        if case['pass_crt']:
            yield (
                CognitiveReflectionTest,
                dict(crt_bat=case['crt_bat'], crt_widget=case['crt_widget'], crt_lake=case['crt_lake']),
            )
        else:
            yield SubmissionMustFail, dict(crt_bat=case['crt_bat'], crt_widget=case['crt_widget'], crt_lake=case['crt_lake'])
            yield CognitiveReflectionTest, dict(crt_bat=1, crt_widget=1, crt_lake=20)

        for value in [self.player.crt_bat, self.player.payoff]:
            expect(value, '!=', None)

