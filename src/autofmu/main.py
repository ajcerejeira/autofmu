"""Main entry point for running the program from the command line."""
import sys
from typing import Optional, Sequence

from autofmu.cli import create_argument_parser


def main(args: Optional[Sequence[str]] = None) -> None:
    """Execute the program in a command line environment.

    Parameters:
        args: sequence of command line arguments
    """
    parser = create_argument_parser()
    options = parser.parse_args(args if args else sys.argv[1:])  # noqa: F841
