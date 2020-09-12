import unittest
from tempfile import NamedTemporaryFile

from fmpy.model_description import read_model_description

from autofmu.generator import generate_model_description


class TestGenerator(unittest.TestCase):
    def test_generate_model_description_generates_valid_model_description(self):
        model_description = generate_model_description(
            model_name="Test Model",
            model_identifier="test-model",
            inputs=["x", "y"],
            outputs=["z"],
        )

        try:
            tmp = NamedTemporaryFile(mode="wb", suffix=".xml", delete=False)
            model_description.write(tmp.name, encoding="utf-8", xml_declaration=True)
            read_model_description(tmp.name, validate_model_structure=True)
        except Exception as e:
            self.fail(e)
        finally:
            tmp.flush()
            tmp.close()


if __name__ == "__main__":
    unittest.main()
