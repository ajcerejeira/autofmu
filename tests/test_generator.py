import os
from pathlib import Path
from tempfile import mkstemp
from uuid import uuid4

import pytest
from fmpy.model_description import read_model_description
from fmpy.validation import validate_fmu

from autofmu.generator import generate_fmu, generate_model_description


def test_generate_model_description_generates_valid_model_description():
    model_description = generate_model_description(
        model_name="Test Model",
        model_identifier="test-model",
        guid=str(uuid4()),
        inputs=["x", "y"],
        outputs=["z"],
    )
    fp, name = mkstemp(suffix=".xml")
    try:
        model_description.write(name, encoding="utf-8", xml_declaration=True)
        read_model_description(name, validate_model_structure=True)
    except Exception as e:
        pytest.fail(str(e))
    finally:
        os.close(fp)


def test_generate_fmu_generates_valid_fmu():
    fp, name = mkstemp(suffix=".fmu")
    generate_fmu("Test Model", ["x", "y"], ["z"], Path(name))
    errors = validate_fmu(name)
    os.close(fp)
    assert not errors
