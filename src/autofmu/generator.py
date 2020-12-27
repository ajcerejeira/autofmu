"""Utilities for generating valid Functional Mockup Units."""

from datetime import datetime
from pathlib import Path
from typing import Iterable
from uuid import uuid4
from zipfile import ZipFile

import pandas
from jinja2 import Environment, FileSystemLoader
from lxml import etree

from autofmu import __version__
from autofmu.strategies import LinearRegressionResult, linear_regression
from autofmu.utils import compile_fmu, slugify


def generate_model_description(
    model_name: str,
    model_identifier: str,
    guid: str,
    inputs: Iterable[str],
    outputs: Iterable[str],
) -> etree.ElementTree:
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
    root = etree.Element(
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
    model_exchange = etree.SubElement(
        root,
        "ModelExchange",
        {"modelIdentifier": model_identifier},
    )
    sourcefiles = etree.SubElement(model_exchange, "SourceFiles")
    etree.SubElement(sourcefiles, "File", {"name": f"{model_identifier}.c"})

    # Co simulation
    co_simulation = etree.SubElement(
        root,
        "CoSimulation",
        {"modelIdentifier": model_identifier},
    )
    sourcefiles = etree.SubElement(co_simulation, "SourceFiles")
    etree.SubElement(sourcefiles, "File", {"name": f"{model_identifier}.c"})

    # Log categories
    log_categories = etree.SubElement(root, "LogCategories")
    etree.SubElement(log_categories, "Category", {"name": "logAll"})
    etree.SubElement(log_categories, "Category", {"name": "logError"})
    etree.SubElement(log_categories, "Category", {"name": "logFmiCall"})
    etree.SubElement(log_categories, "Category", {"name": "logEvent"})

    # Model variables and model structure
    model_variables = etree.SubElement(root, "ModelVariables")
    model_structure = etree.SubElement(root, "ModelStructure")
    model_structure_outputs = etree.SubElement(model_structure, "Outputs")
    model_structure_initial_unknowns = etree.SubElement(
        model_structure,
        "InitialUnknowns",
    )

    for index, variable in enumerate(inputs, 1):
        scalar_variable = etree.SubElement(
            model_variables,
            "ScalarVariable",
            {"name": variable, "valueReference": str(index), "causality": "input"},
        )
        etree.SubElement(scalar_variable, "Real", {"start": "0.0"})
    for index, variable in enumerate(outputs, len(list(inputs)) + 1):
        scalar_variable = etree.SubElement(
            model_variables,
            "ScalarVariable",
            {"name": variable, "valueReference": str(index), "causality": "output"},
        )
        etree.SubElement(scalar_variable, "Real")
        etree.SubElement(
            model_structure_outputs,
            "Unknown",
            {"index": str(index), "dependencies": ""},
        )
        etree.SubElement(
            model_structure_initial_unknowns,
            "Unknown",
            {"index": str(index)},
        )

    return etree.ElementTree(root)


def generate_model_source(
    guid: str,
    inputs: Iterable[str],
    outputs: Iterable[str],
    strategy: str,
    result: LinearRegressionResult,
) -> str:
    """Generate a valid FMI 2.0 C source code implementation.

    Arguments:
        guid: globaly unique identifier that identifies this model
        inputs: variable input names
        outputs: variable output names
        result: a result from an approximation calculation

    Returns:
        Valid C source code that implements the FMI
    """
    env = Environment(
        block_start_string="/*%",
        block_end_string="%*/",
        variable_start_string="/**",
        variable_end_string="**/",
        loader=FileSystemLoader(Path(__file__).parent / "sources"),
        autoescape=True,
    )
    template = env.get_template("fmi2Functions.c")
    return template.render(
        {
            "guid": guid,
            "inputs": inputs,
            "outputs": outputs,
            "strategy": strategy,
            "result": result,
        }
    )


def generate_fmu(
    dataframe: pandas.DataFrame,
    model_name: str,
    inputs: Iterable[str],
    outputs: Iterable[str],
    outfile: Path,
    strategy: str,
) -> None:
    """Generate a valid FMU model.

    Arguments:
        dataframe: dataframe that contains the data used for the approximation
        model_name: name of the model as used in the modeling environment
        inputs: variable input names
        outputs: variable output names
        outfile: path to the file to write the FMU
        strategy: strategy to use to find the approximation (e.g, "linear")
    """
    model_identifier = slugify(model_name)
    guid = str(uuid4())

    with ZipFile(outfile, "w") as fmu:
        # Write model description to the FMU zip file
        model_description = generate_model_description(
            model_name, model_identifier, guid, inputs, outputs
        )
        fmu.writestr(
            "modelDescription.xml",
            etree.tostring(model_description, pretty_print=True),
        )

        # Write header files to the FMU zip file
        headers = (Path(__file__).parent / "sources" / "headers").glob("**/*.h")
        for header in headers:
            fmu.write(str(header), f"sources/headers/{header.name}")

        # Write source files to the FMU zip file
        strategies = {"linear": linear_regression}
        result = strategies[strategy](dataframe, inputs, outputs)

        model_source = generate_model_source(
            guid=guid,
            inputs=inputs,
            outputs=outputs,
            strategy=strategy,
            result=result,
        )
        fmu.writestr("sources/fmi2Functions.c", model_source)

    # Compile the generated source files
    compile_fmu(model_identifier, outfile)
