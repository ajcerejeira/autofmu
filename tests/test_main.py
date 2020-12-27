import pytest
from fmpy.validation import validate_fmu

from autofmu.main import main


def test_main_fails_with_no_arguments():
    with pytest.raises(SystemExit):
        main()


def test_main_generates_valid_fmu(tmp_path, csvfile):
    fmu = str(tmp_path / "model.fmu")
    main([str(csvfile), "--inputs", "x", "y", "--outputs", "z", "-o", fmu])
    errors = validate_fmu(fmu)
    assert not errors
