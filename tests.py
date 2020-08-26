import unittest
from minibot import MiniBot

class TestMessageFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.minibot = MiniBot()

    def test_dict_to_msg(self):
        d = {"key1": 123, "key2": 456, "key_long": 789}
        msg = self.minibot.dictionary_to_msg(d)
        for line in msg.split("\n"):
            self.assertEqual(len(line), len("key_long") + 3 + 3 + 2*len("<code>") + 1)


class TestSendFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.minibot = MiniBot()

    def test_send_dict(self):
        d = {"key1": 123, "key2": 456, "key_long": 789}
        self.minibot.send_dictionary(d, msg="test > send_dictionary")


if __name__ == '__main__':
    unittest.main()