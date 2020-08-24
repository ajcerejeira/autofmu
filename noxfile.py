# flake8: noqa

import nox

nox.options.sessions = ["lint", "typing", "test"]

SOURCE_DIRS = "src", "tests", "noxfile.py"


@nox.session(python=["3.6", "3.7", "3.8"])
def test(session):
    session.install(".")
    session.run("python", "-m", "unittest", *session.posargs)


@nox.session(python=["3.8"])
def coverage(session):
    session.install(".", "coverage[toml]", "codecov")
    session.run("coverage", "run", "-m", "unittest")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


@nox.session
def format(session):
    session.install("black", "isort")
    session.run("black", *SOURCE_DIRS)
    session.run("isort", *SOURCE_DIRS)


@nox.session
def lint(session):
    session.install(
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-isort",
        "flake8",
        "pep8-naming",
    )
    session.run("flake8", *session.posargs, *SOURCE_DIRS)


@nox.session
def typing(session):
    session.install("mypy")
    session.run("mypy", "--ignore-missing-imports", *session.posargs, *SOURCE_DIRS)


@nox.session
def docs(session):
    session.install(".")
    session.install("-r", "docs/requirements.txt")
    session.run(
        "sphinx-build",
        "-M",
        "html",
        "docs",
        "docs/_build",
        "--color",
        "-W",
        *session.posargs,
    )
