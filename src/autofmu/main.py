"""Main entry point for running the program from the command line."""

import logging
import sys
from typing import Optional, Sequence

import pandas

from autofmu.cli import create_argument_parser
from autofmu.generator import generate_fmu


def main(args: Optional[Sequence[str]] = None) -> None:
    """Execute the program in a command line environment.

    Arguments:
        args: sequence of command line arguments
    """
    parser = create_argument_parser()
    options = parser.parse_args(args if args else sys.argv[1:])

    if options.verbose:
        logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    model_name = options.outfile.stem

    logging.info("Reading dataset '%s'", options.dataset)
    dataframe = pandas.read_csv(options.dataset)
    nrows = len(dataframe.index)
    ncols = len(dataframe.columns)
    logging.info("Read %d rows and %d columns from '%s'", nrows, ncols, options.dataset)

    logging.info("Generating FMU '%s'", options.outfile)
    generate_fmu(
        dataframe=dataframe,  # type: ignore
        model_name=model_name,
        inputs=options.inputs,
        outputs=options.outputs,
        outfile=options.outfile,
        strategy=options.strategy,
    )
