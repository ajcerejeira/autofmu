import contextlib
import io
import os
from tempfile import mkstemp

import pytest
from fmpy.validation import validate_fmu

from autofmu.main import main


def test_main_fails_with_no_arguments():
    with pytest.raises(SystemExit):
        main()


def test_main_generates_valid_fmu():
    with contextlib.redirect_stdout(io.StringIO()):
        fp, name = mkstemp()
        main(["data.csv", "--inputs", "x", "y", "--outputs", "z", "-o", name])
        errors = validate_fmu(name)
        os.close(fp)
        assert not errors
