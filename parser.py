# parser pyproject.toml information
import tomli
import sys

if __name__ == "__main__":

    project_path = sys.argv[1]

    with open(project_path, "rb") as f:
        data = tomli.load(f)

    dep_list = []
    for key, value in data["tool"]["poetry"]["dev-dependencies"].items():
        value = value.replace("^", "==")
        dep_list.append(f"{key}{value}")

    pip_deps = " ".join(dep_list)

    sys.stdout.write(f"::set-output name=DEP::{pip_deps}")
