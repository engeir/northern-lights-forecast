"""Nox sessions."""
# import os
import shutil
import tempfile
from pathlib import Path
from textwrap import dedent
from typing import Any

import nox
from nox_poetry import Session
from nox_poetry import session

# from nox import session
# from nox.sessions import Session


# import sys

package = "northern_lights_forecast"
# owner, repository = "engeir", "northern-lights-forecast"
python_versions = ["3.10", "3.9", "3.8"]
nox.options.sessions = (
    "pre-commit",
    "tests",
    "typeguard",
    "xdoctest",
    "docs-build",
)


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages constrained by Poetry's lock file.

    This function is a wrapper for nox.sessions.Session.install. It invokes pip to install
    packages inside of the session's virtualenv. Additionally, pip is passed a constraints
    file generated from Poetry's lock file, to ensure that the packages are pinned to the
    versions specified in poetry.lock. This allows you to manage the packages as Poetry
    development dependencies.

    Parameters
    ----------
    session: Session
        The Session object.
    args: str
        Command-line arguments for pip.
    kwargs: Any
        Additional keyword arguments for Session.install.
    """
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--with",
            "dev",
            "--without-hashes",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        # session.install(f"--constraint={requirements.name}", *args, **kwargs)
        session.install(*args, **kwargs)

    # def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    #     """Install packages constrained by Poetry's lock file."""
    #     requirements = tempfile.NamedTemporaryFile(delete=False)

    #     session.run(
    #         "poetry",
    #         "export",
    #         "--dev",
    #         "--format=requirements.txt",
    #         "--without-hashes",
    #         f"--output={requirements.name}",
    #         external=True,
    #     )
    #     session.install(f"--constraint={requirements.name}", *args, **kwargs)

    # requirements.close()
    # os.unlink(requirements.name)


def activate_virtualenv_in_precommit_hooks(session: Session) -> None:
    """Activate virtualenv in hooks installed by pre-commit.

    This function patches git hooks installed by pre-commit to activate the
    session's virtual environment. This allows pre-commit to locate hooks in
    that environment when invoked from git.

    Parameters
    ----------
    session: Session
        The Session object.
    """
    if session.bin is None:
        return

    virtualenv = session.env.get("VIRTUAL_ENV")
    if virtualenv is None:
        return

    hookdir = Path(".git") / "hooks"
    if not hookdir.is_dir():
        return

    for hook in hookdir.iterdir():
        if hook.name.endswith(".sample") or not hook.is_file():
            continue

        text = hook.read_text()
        bindir = repr(session.bin)[1:-1]  # strip quotes
        if not (
            Path("A") == Path("a") and bindir.lower() in text.lower() or bindir in text
        ):
            continue

        lines = text.splitlines()
        if not (lines[0].startswith("#!") and "python" in lines[0].lower()):
            continue

        header = dedent(
            f"""\
            import os
            os.environ["VIRTUAL_ENV"] = {virtualenv!r}
            os.environ["PATH"] = os.pathsep.join((
                {session.bin!r},
                os.environ.get("PATH", ""),
            ))
            """
        )

        lines.insert(1, header)
        hook.write_text("\n".join(lines))


@session(name="pre-commit", python="3.9")
def precommit(session: Session) -> None:
    """Lint using pre-commit."""
    args = session.posargs or ["run", "--all-files", "--show-diff-on-failure"]
    session.install(
        "black",
        "darglint",
        "flake8",
        "flake8-bandit",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-rst-docstrings",
        "pep8-naming",
        "pre-commit",
        "pre-commit-hooks",
        "reorder-python-imports",
    )
    session.run("pre-commit", *args)
    if args and args[0] == "install":
        activate_virtualenv_in_precommit_hooks(session)


@session(python=python_versions)
def tests(session: Session) -> None:
    """Run the test suite."""
    session.install(".")
    session.install("coverage[toml]", "pytest", "pygments", "scipy")
    try:
        session.run("coverage", "run", "--parallel", "-m", "pytest", *session.posargs)
    finally:
        if session.interactive:
            session.notify("coverage")


@session(python="3.9")
def coverage(session: Session) -> None:
    """Produce the coverage report."""
    # Do not use session.posargs unless this is the only session.
    # nsessions = len(session._runner.manifest)  # type: ignore[attr-defined]
    # has_args = session.posargs and nsessions == 1
    # args = session.posargs if has_args else ["report"]

    # session.install("coverage[toml]")

    install_with_constraints(session, "coverage[toml]", "codecov")
    # if not has_args and any(Path().glob(".coverage.*")):
    #     session.run("coverage", "combine", "--fail-under=0")

    session.run("coverage", "combine")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
    # session.run("codecov", *args)
    # session.run("coverage", *args)


@session(python=python_versions)
def typeguard(session: Session) -> None:
    """Runtime type checking using Typeguard."""
    session.install(".")
    session.install("pytest", "typeguard", "pygments", "scipy")
    session.run("pytest", f"--typeguard-packages={package}", *session.posargs)


@session(python=python_versions)
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    session.install(".")
    session.install("xdoctest[colors]")
    session.run("python", "-m", "xdoctest", package, *args)


@session(name="docs-build", python="3.10")
def docs_build(session: Session) -> None:
    """Build the documentation."""
    args = session.posargs or ["docs", "docs/_build"]
    session.install(".")
    session.install("sphinx", "sphinx-click", "sphinx-rtd-theme")

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-build", *args)


@session(python="3.10")
def docs(session: Session) -> None:
    """Build and serve the documentation with live reloading on file changes."""
    args = session.posargs or ["--open-browser", "docs", "docs/_build"]
    session.install(".")
    session.install("sphinx", "sphinx-autobuild", "sphinx-click", "sphinx-rtd-theme")

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-autobuild", *args)
