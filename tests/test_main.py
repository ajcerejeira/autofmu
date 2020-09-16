import contextlib
import io
import os
import unittest
from tempfile import mkstemp

from fmpy.util import validate_fmu

from autofmu.main import main


class TestMain(unittest.TestCase):
    def test_main_fails_with_no_arguments(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertRaises(SystemExit, main)

    def test_main_generates_valid_fmu(self):
        with contextlib.redirect_stdout(io.StringIO()):
            fp, name = mkstemp()
            main(["data.csv", "--inputs", "x", "y", "--outputs", "z", "-o", name])
            errors = validate_fmu(name)
            os.close(fp)
            self.assertListEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
