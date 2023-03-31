# parse pyproject.toml information
import tomli
import sys
import re


def caret_version(version):
    """Parse a caret version string and return the dependency version."""

    regex_version = r"(\d+).?([0-9.*]+)?$"
    version_match = re.match(regex_version, version)
    major_version = version_match.group(1)
    minor_version = version_match.group(2)

    if int(major_version) > 0 or minor_version is None:
        upper_version = int(major_version) + 1
        version_str = f">={version} <{upper_version}.0.0"
    else:
        version_match = re.match(regex_version, minor_version)
        major_minor_version = version_match.group(1)
        minor_minor_version = version_match.group(2)

        if int(major_minor_version) > 0 or minor_minor_version is None:
            upper_version = int(major_minor_version) + 1
            version_str = f">={version} <0.{upper_version}.0"
        else:
            upper_version = int(minor_minor_version) + 1
            version_str = f">={version} <0.0.{upper_version}"

    return version_str


def modify_string(version_string):
    """Modify a string to be compatible with pip.

    The modification is to be compatible with poetry's dependency
    version format. For caret ("^") and equal ("=") versions. For "~"
    versions, they are replaced by "~=". For >, <, >=, <=, they are
    kept as is.
    """
    if version_string.startswith("~"):
        regex_tilde = r"^~=?\s*([0-9.*]+)$"
        replace_tilde = r"~=\1"
        return re.sub(regex_tilde, replace_tilde, version_string)

    if version_string.startswith("^"):
        regex_caret = r"\^\s*([0-9.*]+)$"
        caret_match = re.match(regex_caret, version_string)
        return caret_version(caret_match.group(1))

    regex = r"^=?\s*([0-9.*]+)$"
    replace = r"==\1"
    dep_str = re.sub(regex, replace, version_string)
    return dep_str


def parse_dependency_dict(dependency_dict):
    """Parse a dependency dictionary and return a string of dependencies."""

    dep_list = []
    for key, value in dependency_dict.items():
        if key == "python":
            continue

        if isinstance(value, dict): # for optional entries
            value = value["version"]

        # the value should be a string
        modified_value = modify_string(value.strip())
        dep_list.append(f"{key}{modified_value}")

    return dep_list


def parse_pyproject(pyproject_data, dependency_path):
    """Parse a pyproject.toml value and return a string of dependencies.

    For poetry style dependencies, the dependency version is adjusted
    to be compatible with pip. For example, "^1.0.0" is converted to "==1.0.0".

    For setuptools style dependencies, the dependency version is kept as is.
    """

    d_path = dependency_path.split(".")
    data = pyproject_data  # not a copy
    for dep in d_path:
        # extract the dependency dictionary
        data = data[dep]

    if isinstance(data, list):
        dep_list = data
    else:
        dep_list = parse_dependency_dict(data)

    return " ".join(dep_list)

def main(project_path, dependency_path):
    """Main function for action."""

    with open(project_path, "rb") as f:
        pyproject_data = tomli.load(f)

    pip_deps = parse_pyproject(pyproject_data, dependency_path)

    sys.stdout.write(f"::set-output name=DEP::{pip_deps}")

if __name__ == "__main__":

    project_path = sys.argv[1]
    dependency_path = sys.argv[2]

    main(project_path, dependency_path)
