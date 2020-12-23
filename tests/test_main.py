from random import random

import pandas
import pytest
from fmpy.validation import validate_fmu

from autofmu.main import main


@pytest.fixture
def csvfile(tmp_path, nrows: int = 10, ncols: int = 5):
    filename = tmp_path / "dataset.csv"
    data = {f"x-{row}": [random() for _ in range(ncols)] for row in range(nrows)}
    dataframe = pandas.DataFrame(data)
    dataframe.to_csv(str(filename))
    return filename


def test_main_fails_with_no_arguments():
    with pytest.raises(SystemExit):
        main()


def test_main_generates_valid_fmu(tmp_path, csvfile):
    fmu = str(tmp_path / "model.fmu")
    main([str(csvfile), "--inputs", "x", "y", "--outputs", "z", "-o", fmu])
    errors = validate_fmu(fmu)
    assert not errors
