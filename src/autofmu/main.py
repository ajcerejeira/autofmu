"""Main entry point for running the program from the command line."""
import sys
from argparse import ArgumentParser, ArgumentTypeError
from pathlib import Path
from shutil import which
from typing import Optional, Sequence

from autofmu import __version__


def main(args: Optional[Sequence[str]] = None) -> None:
    """Execute the program in a command line environment.

    Args:
        args: sequence of command line arguments
    """
    parser = create_argument_parser()
    options = parser.parse_args(args if args else sys.argv[1:])  # noqa: F841


def create_argument_parser() -> ArgumentParser:
    """Create an argument parser object to process command line arguments.

    Returns:
        An argument parser object
    """
    parser = ArgumentParser(prog="autofmu")

    # General options
    parser.add_argument(
        "datasets",
        metavar="FILE",
        nargs="+",
        type=Path,
        help="CSV files that contains the datasets for training the FMU model",
    )
    parser.add_argument(
        "--inputs",
        metavar="VARIABLE",
        nargs="+",
        required=True,
        help="model input variables",
    )
    parser.add_argument(
        "--outputs",
        metavar="VARIABLE",
        nargs="+",
        required=True,
        help="model output variables",
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
    parser.add_argument("--version", action="version", version=__version__)

    # FMU compilation options
    def check_program_exists(program: str) -> str:
        if not which(program):
            raise ArgumentTypeError("'{}' command not found".format(program))
        return program

    fmu_compilation = parser.add_argument_group("FMU compilation options")
    fmu_compilation.add_argument(
        "-s",
        "--skip-compilation",
        action="store_true",
        default=False,
        help="generate FMU model source code without compilling it",
    )
    fmu_compilation.add_argument(
        "-l32",
        "--linux32",
        metavar="COMPILER",
        default=which("i686-linux-gnu-gcc"),
        type=check_program_exists,
        help="path to the Linux 32-bit C compiler (default '%(default)s')",
    )
    fmu_compilation.add_argument(
        "-l64",
        "--linux64",
        metavar="COMPILER",
        default=which("x86_64-linux-gnu-gcc"),
        type=check_program_exists,
        help="path to the Linux 64-bit C compiler (default '%(default)s')",
    )
    fmu_compilation.add_argument(
        "-w32",
        "--win32",
        metavar="COMPILER",
        default=which("i686-w64-mingw32-gcc"),
        type=check_program_exists,
        help="path to the Windows 32-bit C compiler (default '%(default)s')",
    )
    fmu_compilation.add_argument(
        "-w64",
        "--win64",
        metavar="COMPILER",
        default=which("x86_64-w64-mingw32-gcc"),
        type=check_program_exists,
        help="path to the Windows 64-bit C compiler (default '%(default)s')",
    )

    return parser
