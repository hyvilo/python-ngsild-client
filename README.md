# Python NGSI-LD Client

![PyPI version](https://img.shields.io/pypi/v/python-ngsild-client.svg)

pyngsildclient is a Python library dedicated to NGSI-LD.

* [GitHub](https://github.com/hyvilo-it-admin/python-ngsild-client/) | [PyPI](https://pypi.org/project/python-ngsild-client/) | [Documentation](https://hyvilo-it-admin.github.io/python-ngsild-client/)
* Forked from [https://github.com/Orange-OpenSource/python-ngsild-client](https://github.com/Orange-OpenSource/python-ngsild-client) by [Hyvilo](https://www.hyvilo.eu/) | GitHub [@hyvilo](https://github.com/hyvilo-it-admin) | PyPI [@hyvilo](https://pypi.org/user/hyvilo-it-admin/)
* Apache 2.0 License

## Features

* TODO

## Documentation

Documentation is built with [Zensical](https://zensical.org/) and deployed to GitHub Pages.

* **Live site:** https://hyvilo-it-admin.github.io/python-ngsild-client/
* **Preview locally:** `just docs-serve` (serves at http://localhost:8000)
* **Build:** `just docs-build`

API documentation is auto-generated from docstrings using [mkdocstrings](https://mkdocstrings.github.io/).

Docs deploy automatically on push to `main` via GitHub Actions. To enable this, go to your repo's Settings > Pages and set the source to **GitHub Actions**.

## Development

To set up for local development:

```bash
# Clone your fork
git clone git@github.com:hyvilo-it-admin/python-ngsild-client.git
cd python-ngsild-client

# Install in editable mode with live updates
uv tool install --editable .
```

This installs the CLI globally but with live updates - any changes you make to the source code are immediately available when you run `pyngsildclient`.

Run tests:

```bash
uv run pytest
```

Run quality checks (format, lint, type check, test):

```bash
just qa
```

## Author

Python NGSI-LD Client was forked in 2026 by Hyvilo from repository https://github.com/Orange-OpenSource/python-ngsild-client
