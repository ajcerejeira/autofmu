"""Main entry point for running the program from the command line."""
import sys
from typing import Optional, Sequence

from fmpy.util import fmu_info

from autofmu.cli import create_argument_parser
from autofmu.generator import generate_fmu


def main(args: Optional[Sequence[str]] = None) -> None:
    """Execute the program in a command line environment.

    Arguments:
        args: sequence of command line arguments
    """
    parser = create_argument_parser()
    options = parser.parse_args(args if args else sys.argv[1:])

    model_name = options.outfile.stem
    generate_fmu(model_name, options.inputs, options.outputs, options.outfile)

    info = fmu_info(options.outfile)
    print(info)
