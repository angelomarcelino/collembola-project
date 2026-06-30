# Data Contract — animals.json

This document defines the official schema for the data exchanged between the **Scraper** and the **Website** modules.

## Format

- **File:** `scraper/data/animals.json`
- **Type:** JSON array of objects
- **Encoding:** UTF-8

## Schema

| Field                | Type   | Required | Description                          |
|----------------------|--------|----------|--------------------------------------|
| `id`                 | string | ✅       | Unique identifier                    |
| `scientific_name`    | string | ✅       | Scientific name of the species       |
| `common_name`        | string | ✅       | Common/popular name                  |
| `family`             | string | ✅       | Taxonomic family                     |
| `order`              | string | ✅       | Taxonomic order                      |
| `class`              | string | ✅       | Taxonomic class                      |
| `continent`          | string | ✅       | Continent of occurrence              |
| `country`            | string | ✅       | Country of occurrence                |
| `habitat`            | string | ✅       | Primary habitat                      |
| `conservation_status`| string | ✅       | IUCN conservation status code        |
| `description`        | string | ✅       | Brief description of the species     |
| `image`              | string | ✅       | Relative path to the species image   |

## Conservation Status Codes

| Code | Meaning             |
|------|---------------------|
| EX   | Extinct             |
| EW   | Extinct in the Wild |
| CR   | Critically Endangered |
| EN   | Endangered          |
| VU   | Vulnerable          |
| NT   | Near Threatened     |
| LC   | Least Concern       |
| DD   | Data Deficient      |
| NE   | Not Evaluated       |

## Image Convention

The `image` field contains a **relative path** (e.g., `images/mock-001.jpg`). The image file must exist in `scraper/images/` and will be copied into the website build by the CI pipeline.

## Rules

1. Every image referenced in the JSON **must** exist in `scraper/images/`.
2. The `id` field **must** be unique across all records.
3. All string fields **must** be non-empty.
4. The JSON **must** be a valid array (even if empty: `[]`).
