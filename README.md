# sphinx-docs
Build and deploy sphinx documentation based on pyproject.toml parameters.
Currently, the action only parses required packages from pyproject.toml.
The user needs to input the dependency location, i.e. ``tool.poetry.dependencies``.
The parser installs all dependencies including the optional ones.

For poetry style dependencies, the versioning is converted to the pip style. For details on poetry dependencies, please refer to [poetry documentation](https://python-poetry.org/docs/dependency-specification/).

For setuptools dependencies, the user needs to input the dependency list location, to access the dependencies under "[project]" section, the "dependency-path" should be "project.dependencies".

An example of using this action:
To push documentation to the external GitHub page, an ssh key pair needs to be created.
Once ssh key is generated 
([how to generate new ssh key](https://docs.github.com/en/authentication/
connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)),
store the public key in the external repository (settings > security > deploy keys > 
add deploy key). Store the private key in the current repository
(settings > security > secrets > actions > new repository secret) and the secret name
should be "PRIVATE_TOKEN".
