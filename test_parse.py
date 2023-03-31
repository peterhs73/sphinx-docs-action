import pytest
from textwrap import dedent
import tomli
from parse import (
    parse_dependency_dict,
    parse_pyproject,
    modify_string,
    caret_version,
    main,
)


@pytest.mark.parametrize(
    "input_string, expected_output",
    [
        ("1.2.3", '">=1.2.3,<2.0.0"'),
        ("1.2", '">=1.2,<2.0.0"'),
        ("1", '">=1,<2.0.0"'),
        ("0.2.3", '">=0.2.3,<0.3.0"'),
        ("0.0.3", '">=0.0.3,<0.0.4"'),
        ("0.0", '">=0.0,<0.1.0"'),
        ("0", '">=0,<1.0.0"'),
    ],
)
def test_caret_version(input_string, expected_output):
    """Test caret_version() function."""
    assert caret_version(input_string) == expected_output


@pytest.mark.parametrize(
    "input_string, expected_output",
    [
        ("1", "==1"),
        ("1.0", "==1.0"),
        ("1.0.0", "==1.0.0"),
        ("=1.0.0", "==1.0.0"),
        ("= 10.11.12", "==10.11.12"),
        # space in between
        ("=  1.0.0", "==1.0.0"),
        # caret
        ("^ 1.0.0", '">=1.0.0,<2.0.0"'),
        # tilde
        ("~1.0.0", "~=1.0.0"),
        ("~=1.0.0", "~=1.0.0"),
        # wildcard
        ("*", "==*"),
        ("2.*", "==2.*"),
        ("2.0.*", "==2.0.*"),
        # remains the same
        ("==1.0.0", "==1.0.0"),
        (">1.0.0", ">1.0.0"),
        ("<1.0.0", "<1.0.0"),
        ("<=1.0.0", "<=1.0.0"),
        (">=1.0.0", ">=1.0.0"),
        # range of versions
        ("> 1.0.0 < 2.0.0", '"> 1.0.0,< 2.0.0"'),
        ("> 1.0.0,< 2.0.0", '"> 1.0.0,< 2.0.0"'),
        (">= 1.0.0 < 2.0.0", '">= 1.0.0,< 2.0.0"'),
    ],
)
def test_modify_string(input_string, expected_output):
    assert modify_string(input_string) == expected_output


@pytest.fixture
def pyproject_str():
    """Return a sample pyproject.toml value."""

    pyproject_toml = """\
    [tool.poetry.dependencies]
    python = ">=3.8"
    tomli = ">=2.0.0"
    tox = { version = "=3.24.5", optional = true }
    tox-gh-actions = { version = "==2.10.0", optional = true }
    sphinx = { version = "^6.1.3", optional = true }
    sphinx-rtd-theme = { version = " ~ 1.0.0", optional = true }

    [project]
    dependencies = [
        "docutils",
        "BazSpam == 1.1",
    ]
    """

    return pyproject_toml


@pytest.fixture
def pyproject_value(pyproject_str):
    """Return a sample pyproject.toml value."""

    return tomli.loads(dedent(pyproject_str))


def test_parse_dependency_dict(pyproject_value):
    """Test parse_dependency_dict() function."""

    dependency_dict = pyproject_value["tool"]["poetry"]["dependencies"]
    expected = [
        "tomli>=2.0.0",
        "tox==3.24.5",
        "tox-gh-actions==2.10.0",
        'sphinx">=6.1.3,<7.0.0"',
        "sphinx-rtd-theme~=1.0.0",
    ]

    assert parse_dependency_dict(dependency_dict) == expected


def test_parse_pyproject(pyproject_value):
    """Test parse_pyproject() function."""

    expected_poetry = (
        "tomli>=2.0.0 tox==3.24.5 tox-gh-actions==2.10.0 "
        'sphinx">=6.1.3,<7.0.0" sphinx-rtd-theme~=1.0.0'
    )
    expected_stanard = "docutils BazSpam == 1.1"
    assert (
        parse_pyproject(pyproject_value, "tool.poetry.dependencies") == expected_poetry
    )
    assert parse_pyproject(pyproject_value, "project.dependencies") == expected_stanard


def test_main(tmp_path, pyproject_str, capsys):

    toml_path = tmp_path / "pyproject.toml"

    with open(toml_path, "w") as f:
        f.write(pyproject_str)

    expected_poetry = (
        "::set-output name=DEP::"
        "tomli>=2.0.0 tox==3.24.5 tox-gh-actions==2.10.0 "
        'sphinx">=6.1.3,<7.0.0" sphinx-rtd-theme~=1.0.0'
    )
    main(str(toml_path), "tool.poetry.dependencies")
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_poetry
