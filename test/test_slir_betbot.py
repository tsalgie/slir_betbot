from slir_betbot import SLIRBetbot
import unittest2


class TestSLIRBetbot(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        streamlabs_parent = None
        command = "!bet"
        currency = "ploods"
        iracing_user = 'Complx'

        cls.betbot = SLIRBetbot(streamlabs_parent, command, iracing_user, currency)

    @classmethod
    def tearDownClass(cls):
        cls.betbot = None

    def test_betbot(self):
        self.betbot.add_bet('test_user', 'win', 10000, 3.5)
        assert self.betbot.bets == {'test_user': ('win', 10000, 3.5)}


if __name__ == '__main__':
    unittest2.main()
