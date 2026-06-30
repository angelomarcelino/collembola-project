# Collembola Scraper

Web scraper for extracting Collembola (springtail) species data.

## Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation)

## Setup

```bash
cd scraper
poetry install
```

## Usage

```bash
poetry run python src/scraper.py
```

## Output

The scraper produces:

- `data/animals.json` — species data following the [data contract](../docs/data-contract.md)
- `images/` — downloaded species images referenced in the JSON

## Running via GitHub Actions

The scraper can also be triggered manually via the **Run Scraper** workflow in GitHub Actions (workflow_dispatch).
