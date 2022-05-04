# AWS SNS Subscription Manager

[![PyPI](https://img.shields.io/pypi/v/sns-sub-manager.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/sns-sub-manager.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/sns-sub-manager)][python version]
[![License](https://img.shields.io/pypi/l/sns-sub-manager)][license]

[![Read the documentation at https://sns-sub-manager.readthedocs.io/](https://img.shields.io/readthedocs/sns-sub-manager/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/andrewthetechie/sns-sub-manager/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/andrewthetechie/sns-sub-manager/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/sns-sub-manager/
[status]: https://pypi.org/project/sns-sub-manager/
[python version]: https://pypi.org/project/sns-sub-manager
[read the docs]: https://sns-sub-manager.readthedocs.io/
[tests]: https://github.com/andrewthetechie/sns-sub-manager/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/andrewthetechie/sns-sub-manager
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Features

- Allows someone to subscribe and unsubscribe to sns topics via a rest api
- Configure what SNS topics to manage via a YAML file
- Per topic configuration of what types of subscriptions to accept
- Able to turn off unsubscribe globally
- No auth - that's your problem!
- Docker image you can run easily

## Requirements

- TODO

## Installation

You can install _AWS SNS Subscription Manager_ via [pip] from [PyPI]:

```console
$ pip install sns-sub-manager
```

## Usage

You probably don't want to be using this to be honest.

Someday, there will be info here. For today...

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_AWS SNS Subscription Manager_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/andrewthetechie/sns-sub-manager/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/andrewthetechie/sns-sub-manager/blob/main/LICENSE
[contributor guide]: https://github.com/andrewthetechie/sns-sub-manager/blob/main/CONTRIBUTING.md
[command-line reference]: https://sns-sub-manager.readthedocs.io/en/latest/usage.html
