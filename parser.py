"""Parse pyproject information"""
import os
import tomli

project_path = os.environ.get("pyproject_path")

with open(project_path, "rb") as f:
    data = tomli.load(f)
    print(data["tool"]["poetry"]["version"])
