# sphinx-docs
Build and deploy sphinx documentation based on pyproject.toml parameters.

Current the action only parses required packages from pyproject.toml. The packages
needs to be listed under `tool.poetry.dev-dependencies`.

An example of using this action:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        uses: peterhs73/sphinx-docs-action@v0.0.1
        with:
          python-version: 3.8 # defaults to 3.8
          pyproject-path: pyproject.toml # defaults to pyproject.toml
          docs-source: docs/ # defaults to docs/
          docs-build: docs_build/ # defaults to docs_build/
          external-repo: <username>/<repo-name>
          external-repo-branch: gh-pages # defaults to master
          deploy-token: ${{ secrets.PRIVATE_TOKEN}}
```

To push documentations to the external github page, an ssh key pair needs to be created.
Once ssh key are generated 
([how to generate new ssh key](https://docs.github.com/en/authentication/
connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)),
store the public key in the external repository (settings > security > deploy keys > 
add deploy key). Store the private key in the current repository
(settings > security > secrets > actions > new repository secret) and the secret name
should be "PRIVATE_TOKEN".
