import os
import unittest
from tempfile import mkstemp
from uuid import uuid4

from fmpy.model_description import read_model_description
from fmpy.util import validate_fmu

from autofmu.generator import generate_fmu, generate_model_description


class TestGenerator(unittest.TestCase):
    def test_generate_model_description_generates_valid_model_description(self):
        model_description = generate_model_description(
            model_name="Test Model",
            model_identifier="test-model",
            guid=str(uuid4()),
            inputs=["x", "y"],
            outputs=["z"],
        )
        try:
            fp, name = mkstemp(suffix=".xml")
            model_description.write(name, encoding="utf-8", xml_declaration=True)
            read_model_description(name, validate_model_structure=True)
        except Exception as e:
            self.fail(e)
        finally:
            os.close(fp)

    def test_generate_fmu_generates_valid_fmu(self):
        fp, name = mkstemp(suffix=".fmu")
        generate_fmu("Test Model", ["x", "y"], ["z"], name)
        errors = validate_fmu(name)
        os.close(fp)
        self.assertListEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
