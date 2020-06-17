"""Test module for :py:mod:`autofmu.main`."""
import contextlib
import io
import unittest

from autofmu.main import main


class TestMain(unittest.TestCase):
    """Test class for :py:mod:`autofmu.main`."""

    def test_main_fails_with_no_arguments(self):
        """Tests the main entry point fails when called without arguments."""
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertRaises(SystemExit, main)


if __name__ == "__main__":
    unittest.main()
