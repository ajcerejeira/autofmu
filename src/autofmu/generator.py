"""Utilities for generating valid Functional Mockup Units."""
import xml.etree.ElementTree as ET  # noqa: N
from datetime import datetime
from pathlib import Path
from typing import Iterable
from uuid import uuid4
from zipfile import ZipFile

from jinja2 import Environment, FileSystemLoader

from autofmu import __version__
from autofmu.utils import compile_fmu, pretty_print_xml, slugify


def generate_model_description(
    model_name: str,
    model_identifier: str,
    guid: str,
    inputs: Iterable[str],
    outputs: Iterable[str],
) -> ET.ElementTree:
    """Generate a valid FMI 2.0 model description XML document.

    Arguments:
        model_name: name of the model as used in the modeling environment
        model_identifier: short class name according to C syntax, for example, "A_B_C"
        guid: globaly unique identifier that identifies this model
        inputs: variable input names
        outputs: variable output names

    Returns:
        Valid FMI 2.0 model description XML document
    """
    root = ET.Element(
        "fmiModelDescription",
        attrib={
            "fmiVersion": "2.0",
            "modelName": model_name,
            "guid": guid,
            "generationTool": f"autofmu {__version__}",
            "generationDateAndTime": datetime.utcnow().isoformat(),
        },
    )

    # Model exchange
    model_exchange = ET.SubElement(
        root, "ModelExchange", {"modelIdentifier": model_identifier}
    )
    sourcefiles = ET.SubElement(model_exchange, "SourceFiles")
    ET.SubElement(sourcefiles, "File", {"name": f"{model_identifier}.c"})

    # Co simulation
    co_simulation = ET.SubElement(
        root, "CoSimulation", {"modelIdentifier": model_identifier}
    )
    sourcefiles = ET.SubElement(co_simulation, "SourceFiles")
    ET.SubElement(sourcefiles, "File", {"name": f"{model_identifier}.c"})

    # Model variables and model structure
    model_variables = ET.SubElement(root, "ModelVariables")
    model_structure = ET.SubElement(root, "ModelStructure")
    model_structure_outputs = ET.SubElement(model_structure, "Outputs")
    model_structure_initial_unknowns = ET.SubElement(model_structure, "InitialUnknowns")

    for index, variable in enumerate(inputs, 1):
        scalar_variable = ET.SubElement(
            model_variables,
            "ScalarVariable",
            {"name": variable, "valueReference": str(index), "causality": "input"},
        )
        ET.SubElement(scalar_variable, "Real", {"start": "0.0"})
    for index, variable in enumerate(outputs, len(list(inputs)) + 1):
        scalar_variable = ET.SubElement(
            model_variables,
            "ScalarVariable",
            {"name": variable, "valueReference": str(index), "causality": "output"},
        )
        ET.SubElement(scalar_variable, "Real")
        ET.SubElement(model_structure_outputs, "Unknown", {"index": str(index)})
        ET.SubElement(
            model_structure_initial_unknowns, "Unknown", {"index": str(index)}
        )

    return ET.ElementTree(root)


def generate_model_source(
    guid: str, inputs: Iterable[str], outputs: Iterable[str]
) -> str:
    """Generate a valid FMI 2.0 C source code implementation.

    Arguments:
        guid: globaly unique identifier that identifies this model
        inputs: variable input names
        outputs: variable output names

    Returns:
        Valid C source code that implements the FMI
    """
    env = Environment(
        loader=FileSystemLoader(Path(__file__).parent / "sources"), autoescape=True
    )
    template = env.get_template("fmi2Functions.c")
    return template.render({"guid": guid, "inputs": inputs, "outputs": outputs})


def generate_fmu(
    model_name: str, inputs: Iterable[str], outputs: Iterable[str], outfile: Path
) -> None:
    """Generate a valid FMU model.

    Arguments:
        model_name: name of the model as used in the modeling environment
        inputs: variable input names
        outputs: variable output names
        outfile: path to the file to write the FMU
    """
    model_identifier = slugify(model_name)
    guid = str(uuid4())

    with ZipFile(outfile, "w") as fmu:
        # Write model description to the FMU zip file
        model_description = generate_model_description(
            model_name, model_identifier, guid, inputs, outputs
        )
        fmu.writestr(
            "modelDescription.xml", pretty_print_xml(model_description.getroot())
        )

        # Write header files to the FMU zip file
        headers = (Path(__file__).parent / "sources" / "headers").glob("**/*.h")
        for header in headers:
            fmu.write(str(header), f"sources/headers/{header.name}")

        # Write source files to the FMU zip file
        model_source = generate_model_source(guid, inputs, outputs)
        fmu.writestr("sources/fmi2Functions.c", model_source)

    # Compile the generated source files
    compile_fmu(model_identifier, outfile)
