# Collembola Project

An interactive catalog of Collembola (springtail) species, composed of two independent modules:

| Module | Description | Tech |
|--------|-------------|------|
| [Scraper](./scraper/) | Extracts species data from the web | Python + Poetry |
| [Website](./website/) | Displays species data interactively | React + Vite |

## Delevoped by:

ANGELO MARCELINO CORDEIRO;
GUILHERME FÉLIX DE MEDEIROS BRANDT;
MARCUS VINICIUS SILVA NUNES.

## Presentation:

[https://www.youtube.com/watch?v=QIE9LiR4oto](https://www.youtube.com/watch?v=QIE9LiR4oto)

## Architecture

The modules are fully decoupled. The only integration point is a **data contract** ([`docs/data-contract.md`](./docs/data-contract.md)).

```
Website
   ▲
   │
animals.json  ← data contract
   │
Scraper
   │
   ▼
Original Site
```

## Quick Start

### Scraper

```bash
cd scraper
poetry install
poetry run python src/scraper.py
```

### Website

```bash
cd website
npm install
npm run dev
```

## Deployment

The website is deployed automatically to GitHub Pages via GitHub Actions on every push to `main`.

To configure, go to **Settings → Pages → Source** and select **GitHub Actions**.

## Project Structure

```
├── scraper/                 # Data extraction module
│   ├── src/                 # Scraper source code
│   ├── data/                # Output: animals.json
│   ├── images/              # Output: downloaded images
│   └── pyproject.toml       # Poetry config
│
├── website/                 # Frontend module
│   ├── src/                 # React source code
│   ├── public/              # Static assets
│   └── package.json         # npm config
│
├── .github/workflows/       # CI/CD
│   ├── scraper.yml          # Manual scraper trigger
│   └── deploy.yml           # Auto-deploy website
│
└── docs/
    └── data-contract.md     # Official data schema
```

## Team Rules

- **Team A (Scraper):** only modifies files inside `scraper/` and `docs/`
- **Team B (Website):** only modifies files inside `website/`
- Changes to `animals.json` schema must be communicated before implementation
