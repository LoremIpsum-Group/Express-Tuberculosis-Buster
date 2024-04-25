import unittest

class TestDigit(unittest.TestCase):
    def setUp(self):
        # *in the future this would mean that testing each components happens here
        self.digit = 5

    def test_digit(self):
        self.assertEqual(self.digit, 6)


if __name__ == "__main__":
    # *will result into failure
    unittest.main()
