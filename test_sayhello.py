
import unittest
from hello import sayhello


class SayHelloTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sayhello(self):
        rv = sayhello()
        self.assertEqual(rv, 'Hello,stranger:)')

    def test_sayhello_to_someone(self):
        rv = sayhello(to='Grey')
        self.assertEqual(rv, 'Hello,Grey:)')

if __name__ == '__main__':
    unittest.main()