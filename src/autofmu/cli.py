"""Utilities for exposing a command line interface of the program."""

from argparse import ArgumentParser
from pathlib import Path

from autofmu import __version__


def create_argument_parser() -> ArgumentParser:
    """Create an argument parser object to process command line arguments.

    Returns:
        An argument parser object
    """
    parser = ArgumentParser(prog="autofmu")

    # General options
    parser.add_argument(
        "dataset",
        metavar="FILE",
        type=Path,
        help="CSV files that contain the datasets for training the FMU model",
    )
    parser.add_argument(
        "-o",
        "--outfile",
        metavar="FILE",
        type=Path,
        default=Path("model.fmu"),
        help="file to output the generated FMU model (default '%(default)s')",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        default=False,
        action="store_true",
        help="run the program in verbose mode",
    )
    parser.add_argument("-V", "--version", action="version", version=__version__)
    parser.add_argument(
        "--inputs",
        metavar="VARIABLE",
        required=True,
        nargs="+",
        help="list of names of the model input variables",
    )
    parser.add_argument(
        "--outputs",
        metavar="VARIABLE",
        required=True,
        nargs="+",
        help="list of names of the model output variables",
    )
    parser.add_argument(
        "-s",
        "--strategy",
        choices=["linear", "logistic"],
        default="linear",
        help="strategy to use to deduce the approximation",
    )

    return parser
