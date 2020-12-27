from uuid import uuid4

import pandas
import pytest
from fmpy.model_description import read_model_description
from fmpy.validation import validate_fmu

from autofmu.generator import generate_fmu, generate_model_description


def test_generate_model_description_generates_valid_model_description(tmp_path):
    filename = str(tmp_path / "modelDescription.xml")
    model_description = generate_model_description(
        model_name="Test Model",
        model_identifier="test-model",
        guid=str(uuid4()),
        inputs=["x", "y"],
        outputs=["z"],
    )
    try:
        model_description.write(filename, encoding="utf-8", xml_declaration=True)
        read_model_description(filename, validate_model_structure=True)
    except Exception as e:
        pytest.fail(str(e))


def test_generate_fmu_generates_valid_fmu(tmp_path, csvfile):
    fmu = tmp_path / "model.fmu"
    dataframe = pandas.read_csv(csvfile)
    generate_fmu(
        dataframe=dataframe,  # type: ignore
        model_name="Test Model",
        inputs=["x", "y"],
        outputs=["z"],
        outfile=fmu,
        strategy="linear",
    )
    errors = validate_fmu(fmu)
    assert not errors
