# Collembola Website

Interactive website for browsing Collembola species data.

Built with React + Vite. Deployed as a static site on GitHub Pages.

## Prerequisites

- Node.js 20+
- npm

## Setup

```bash
cd website
npm install
```

## Development

```bash
npm run dev
```

## Build

```bash
npm run build
```

The production build outputs to `dist/`.

## Data

The website consumes `data/animals.json` from its `public/` directory. In production, the GitHub Actions workflow copies this file from `scraper/data/` automatically.

For local development, you can copy it manually:

```bash
mkdir -p public/data public/images
cp ../scraper/data/animals.json public/data/
cp -r ../scraper/images/. public/images/
```

See the [data contract](../docs/data-contract.md) for the JSON schema.
