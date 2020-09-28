"""General utilities."""
import re
import shutil
import subprocess
import unicodedata
import xml.dom.minidom as minidom  # noqa: S
import xml.etree.ElementTree as ET  # noqa: N
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Mapping, Optional
from zipfile import ZipFile


def slugify(value, allow_unicode=False):
    """Convert a string to a URL slug.

    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.

    See also:
        https://docs.djangoproject.com/en/3.1/ref/utils/#django.utils.text.slugify
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def pretty_print_xml(element: ET.Element) -> str:
    """Transform a XML element into a well formatted and human readable string.

    Arguments:
        element: XML element to pretty print

    Returns:
        string that contains the pretty printed dump of the XML elements
    """
    dump = ET.tostring(element, encoding="utf-8", xml_declaration=True)
    return minidom.parseString(dump).toprettyxml(indent="    ")  # noqa: S


def run_cmake(
    source_dir: Path, build_dir: Path, variables: Optional[Mapping[str, str]] = None
):
    """Run cmake command and build the targets.

    Roughly equivalent to running the following two commands:

    .. code-block:: shell

       cmake -S source_dir -B build_dir
       cmake --build build_dir

    Arguments:
        source_dir: path to source directory
        build_dir: path to build directory
        variables: a mapping between variable names and their values, e.g,
            ``{"CMAKE_PROJECT_NAME": "Unicorn"}`` would be passed as
            ``DCMAKE_PROJECT_NAME=Unicorn`` in the command line
    """
    cmake = shutil.which("cmake") or "cmake"
    if variables:
        args = [f"-D{name}={value}" for name, value in variables.items()]
    else:
        args = []
    subprocess.run(
        [cmake, *args, "-S", source_dir, "-B", build_dir],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.run(
        [cmake, "--build", build_dir],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def compile_fmu(model_identifier: str, fmu_path: Path):
    """Compile the C sources files of an FMU.

    Extracts the FMU into a temporary directory, calling cmake to build the FMU,
    copying the generated library back into the FMU file.
    If `MinGW <http://www.mingw.org/>`_ is installed, it also cross compiles
    the FMU for Linux and Windows.

    Arguments:
        model_identifier: short class name according to C syntax, for example, "A_B_C"
        fmu_path: path to the FMU file
    """
    with ZipFile(fmu_path, "a") as fmu, TemporaryDirectory() as tmpdir:
        fmu.extractall(tmpdir)

        # Use CMake to compile the FMU for the current platform
        shutil.copy(Path(__file__).parent / "cmake" / "CMakeLists.txt", tmpdir)
        build_dir = Path(tmpdir) / "build"
        run_cmake(Path(tmpdir), build_dir, {"CMAKE_PROJECT_NAME": model_identifier})

        # Cross compile
        compilers = (
            ("i686-linux-gnu-gcc", "Linux"),
            ("x86_64-linux-gnu-gcc", "Linux"),
            ("i686-w64-mingw32-gcc", "Windows"),
            ("x86_64-w64-mingw32-gcc", "Windows"),
        )
        for compiler, system in compilers:
            run_cmake(
                Path(tmpdir),
                build_dir / compiler,
                {
                    "CMAKE_PROJECT_NAME": model_identifier,
                    "CMAKE_SYSTEM_NAME": system,
                    "CMAKE_C_COMPILER": compiler,
                },
            )
        for lib in Path(tmpdir).glob("binaries/**/*"):
            fmu.write(lib, lib.relative_to(tmpdir))
