import unittest

# AC 3.2: Given the size or type has not been selected, when the player attempts
# to start the game, then the system prevents it and displays a prompt.
# STATUS: SKIPPED — board size and type are hardcoded this sprint (English, 7)

class TestAC3_2(unittest.TestCase):
    @unittest.skip("Not applicable this sprint — size and type are hardcoded to English 7")
    def test_missing_size_or_type_prevents_start(self):
        pass

if __name__ == "__main__":
    unittest.main()
