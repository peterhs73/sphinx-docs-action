# sphinx-docs
Build and deploy sphinx documentation based on pyproject.toml parameters.
Currently, the action only parses required packages from pyproject.toml.
The user needs to input the dependency location, i.e. "tool.poetry.dependencies".
The parser installs all dependencies including the optional ones.

For poetry style dependencies, the versioning is converted to the pip style. For details on poetry dependencies, please refer to [poetry documentation](https://python-poetry.org/docs/dependency-specification/).

For setuptools dependencies, the user needs to input the dependency list location, to access the dependencies under "[project]" section, the "dependency-path" should be "project.dependencies".

Please see the action.yaml input section for all the input information.

An example of using this action, triggered when a release is published:

```yaml
name: Build and publish to github repo

on:
  release:
    types: [published]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        uses: peterhs73/sphinx-docs-action@v0.1.0
        with:
          docs-source: docs/
          dependency-path: tool.poetry.dependencies
          external-repo: peterhs73/sphinx-docs
          deploy-token: ${{secrets.PRIVATE_TOKEN}}

```


To push documentation to the external GitHub page, an ssh key pair needs to be created.
Once ssh key is generated 
([how to generate new ssh key](https://docs.github.com/en/authentication/
connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)),
store the public key in the external repository (settings > security > deploy keys > 
add deploy key). Store the private key in the current repository
(settings > security > secrets > actions > new repository secret) and the secret name
should be "PRIVATE_TOKEN".
