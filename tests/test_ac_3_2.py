import pytest
from Model.board import Board

# AC 3.2: Given the size or type has not been selected (or is invalid),
# when the player attempts to start the game,
# then the system prevents it and displays a prompt.
# STATUS: PASSES — Board raises ValueError for invalid size/type;
#         view layer (main_window) catches this and shows an error dialog.

class TestAC3_2:
    def test_invalid_size_raises_error(self):
        with pytest.raises(ValueError):
            Board(size=2)

    def test_non_integer_size_raises_error(self):
        with pytest.raises((ValueError, TypeError)):
            Board(size="abc")

    def test_invalid_type_raises_error(self):
        with pytest.raises(ValueError):
            Board(type="triangle", size=7)

    def test_valid_size_and_type_does_not_raise(self):
        board = Board(type="english", size=7)
        assert board is not None
