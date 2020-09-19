"""General utilities."""
import platform
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path
from tempfile import TemporaryDirectory
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


def compile_fmu(model_identifier: str, fmu_path: Path):
    """Compile the C sources files of an FMU.

    Extracts the FMU into a temporary directory, calling cmake to build the FMU,
    copying the generated library back into the FMU file.

    Arguments:
        model_identifier: short class name according to C syntax, for example, "A_B_C"
        fmu_path: path to the FMU file
    """
    with ZipFile(fmu_path, "a") as fmu, TemporaryDirectory() as tmpdir:
        cmake_build_dir = Path(tmpdir) / "build"
        fmu.extractall(tmpdir)

        # Use CMake to compile the FMU
        shutil.copy(Path(__file__).parent / "cmake" / "CMakeLists.txt", tmpdir)
        subprocess.run(
            [
                shutil.which("cmake") or "cmake",
                f"-DCMAKE_PROJECT_NAME={model_identifier}",
                "-S",
                tmpdir,
                "-B",
                str(cmake_build_dir),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        subprocess.run(
            [shutil.which("cmake") or "cmake", "--build", str(cmake_build_dir)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )

        # Copy the generated library to the zip file
        arch = 64 if sys.maxsize > 2 ** 32 else 32
        system = platform.system()
        if system == "Windows":
            build_dir = f"build/win{arch}"
        else:
            build_dir = f"build/{system.lower()}{arch}"

        library = next(cmake_build_dir.glob(f"{model_identifier}.*"))
        fmu.write(str(library), f"{build_dir}/{library.name}")
