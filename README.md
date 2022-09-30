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
          python-version: 3.10 # defaults to 3.8
          pyproject-path: pyproject.toml # defaults to pyproject.toml
          docs-source: docs/source/ # defaults to docs/
          docs-build: docs_build/ # defaults to docs_build/
          external-repo: <username>/<repo-name>
          external-repo-branch: gh-pages # defaults to master
          deploy-token: ${{ secrets.PRIVATE_TOKEN}}
```
