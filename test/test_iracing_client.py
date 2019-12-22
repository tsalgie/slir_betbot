from iracing_client import IracingClient
import unittest2


class TestIracingClient(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = IracingClient()

    @classmethod
    def tearDownClass(cls):
        cls.client = None

    def test_client(self):
        pass


if __name__ == '__main__':
    unittest2.main()
