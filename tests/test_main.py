import contextlib
import io
import unittest

from autofmu.main import main


class TestMain(unittest.TestCase):
    def test_main_fails_with_no_arguments(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertRaises(SystemExit, main)


if __name__ == "__main__":
    unittest.main()
