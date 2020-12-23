"""Nox configuration file.

For more information on this file, see
https://nox.thea.codes/
"""

import nox

nox.options.sessions = ["lint", "typing", "test"]


@nox.session(python=["3.6", "3.7", "3.8"])
def test(session):
    """Run tests."""
    session.install(".")
    session.run("python", "-m", "unittest", *session.posargs)


@nox.session(python=["3.8"])
def coverage(session):
    """Run tests with coverage report."""
    session.install(".", "coverage[toml]", "codecov")
    session.run("coverage", "run", "-m", "unittest")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


@nox.session
def lint(session):
    """Lint the code with black, isort, pylint and pydocstyle."""
    session.install(".[lint]")
    session.run("flake8", *session.posargs)


@nox.session
def typing(session):
    """Type chec the program with mypy."""
    session.install(".[typing]")
    session.run("mypy", "src/", "tests/")


@nox.session
def docs(session):
    """Build documentation with sphinx."""
    session.install(".[docs]")

    sphinx_args = ["docs", "docs/_build", "-W"]

    if "serve" in session.posargs:
        session.run("sphinx-autobuild", *sphinx_args)
    else:
        session.run("sphinx-build", *sphinx_args)
