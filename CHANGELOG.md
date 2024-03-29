# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2023-04-02

0.2.0 moves away from the toml parsing, but install the current package and optional dependencies separately. Use version 0.1.1 if only want to install dependencies.

### Changed
- Remove parse.py and install the package directly.
- "pyproject-path" specifies the extras.

## [0.1.1] - 2023-03-31

### Changed
- Bump actions/checkout from v2 to v3.
- Bump actions/setup-python from v3 to v4.
- Change set-output to the new actions command style.

## [0.1.0] - 2023-03-31

### Added

- Add support for setuptools style dependencies.
- Add support for poetry style dependencies.
- Add unit tests.

### Changed
- Allow the repository to specify the dependency location.
- Change the parse file name to "parse.py" to avoid stdlib naming collision.

## [0.0.2]

### Fixed
- Fix the issue that the parser.py file cannot be found.
