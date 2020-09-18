"""Utilities for generating valid Functional Mockup Units."""
from datetime import datetime
from pathlib import Path
from typing import Iterable
from uuid import uuid4
from zipfile import ZipFile

from lxml import etree as ET  # noqa: N, S

from autofmu import __version__
from autofmu.utils import slugify


def generate_model_description(
    model_name: str,
    model_identifier: str,
    inputs: Iterable[str],
    outputs: Iterable[str],
) -> ET.ElementTree:
    """Generate a valid FMI 2.0 model description XML document.

    Arguments:
        model_name: name of the model as used in the modeling environment
        model_identifier: Short class name according to C syntax, for example, "A_B_C"
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
            "guid": str(uuid4()),
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

    with ZipFile(outfile, "w") as fmu:
        # Write model description to the FMU zip file
        with fmu.open("modelDescription.xml", "w") as model_description_file:
            model_description = generate_model_description(
                model_name, model_identifier, inputs, outputs
            )
            model_description.write(
                model_description_file,
                encoding="utf-8",
                xml_declaration=True,
                pretty_print=True,
            )

        # Write header files to the FMU zip file
        headers = (Path(__file__).parent / "sources" / "headers").glob("**/*.h")
        for header in headers:
            fmu.write(str(header), f"sources/headers/{header.name}")

        # Write source files to the FMU zip file
        # TODO

    # Compile the generated source files
    # TODO
