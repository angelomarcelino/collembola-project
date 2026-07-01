# Implementation Plan — Develop Collembola Scraper

This plan describes the implementation of the Collembola (springtail) web scraper module. The scraper will extract taxonomic, geographic, and habitat data for all accepted Collembola species from the official **Catálogo Taxonômico da Fauna do Brasil (CTFB)** REST API maintained by the Jardim Botânico do Rio de Janeiro (JBRJ) at `fauna.jbrj.gov.br`.

## Proposed Design & Architecture

Rather than scraping dynamic HTML pages (which requires complex session handling, pagination, and HTML parsing), we will query the official and fast JBRJ REST API endpoints directly:
1.  **Species List & Taxonomy:** Query `https://fauna.jbrj.gov.br/rest/v_taxonomia_hierarquia?class=eq.Collembola&taxonRank=eq.species` to fetch all 516 accepted species with their full taxonomic ranks (Order/Suborder, Family, Genus, Scientific Name).
2.  **Habitats & Life Forms:** Query `/v_forma_de_vida_e_substrato` in batches to fetch the environment of occurrence.
3.  **Distributions:** Query `/v_distribuicao` in batches to aggregate the occurrence locations (Brazilian states).
4.  **Images:** The JBRJ database does not contain images for Collembola species. To comply with the data contract requirement that every referenced image must exist and the string must be non-empty, we will:
    *   Generate a beautiful, premium placeholder image (`placeholder.jpg`) representing a springtail illustration/microscope scan using AI image generation.
    *   Save this image to `scraper/images/placeholder.jpg`.
    *   Set the `image` field of every species to `images/placeholder.jpg`.
    *   Ensure the code is prepared to download custom species images if the JBRJ image endpoints return them in the future.

---

## User Review Required

> [!IMPORTANT]
> **Data Size & Execution Time:** The scraper will extract approximately 516 species. Performing batch requests for habitats and distributions will take about 10–20 seconds in total.
> We will cache API requests in memory during the execution to optimize performance and prevent rate limiting.

---

## Proposed Changes

### Scraper Module

#### [MODIFY] [scraper.py](file:///c:/Users/Guilherme/Documents/GitHub/collembola-project/scraper/src/scraper.py)
*   Implement the `scrape()` function:
    1.  Fetch the complete list of accepted Collembola species from `/v_taxonomia_hierarquia`.
    2.  Extract the species IDs (`taxonID`) and query their distributions and habitats in batch chunks (e.g., 50 species per batch request) to speed up execution.
    3.  Map Portuguese taxonomic terms, states, and environments to English/readable values:
        *   `subOrder` -> `order` (e.g. `Poduromorpha`, `Symphypleona`)
        *   `family` -> `family`
        *   `class` -> `class` (Collembola)
        *   `locationID` (e.g., `BR-RJ`, `BR-AM`) -> Full state names (e.g., `Rio de Janeiro, Amazonas`) in the `country` field (formatted as `Brazil (Rio de Janeiro, Amazonas)`).
        *   `habitat` (e.g., `TERRESTRE`) -> mapped to `"Terrestrial"`, `"Freshwater"`, etc.
        *   `conservation_status` -> defaulted to `"NE"` (Not Evaluated) since conservation status is handled by a separate platform (ICMBio Salve) and not CTFB.
        *   `common_name` -> defaulted to `"Springtail"` since species-level common names do not exist in the database.
    4.  Save the generated array to `scraper/data/animals.json`.
    5.  Check for custom species images using the JBRJ image endpoints. If found, download them; otherwise, set the path to `images/placeholder.jpg`.

#### [NEW] [placeholder.jpg](file:///c:/Users/Guilherme/Documents/GitHub/collembola-project/scraper/images/placeholder.jpg)
*   A high-quality placeholder illustration for springtails, satisfying the data contract that every referenced image must exist under `scraper/images/`.

---

## Verification Plan

### Automated Tests
*   Run the scraper locally and verify that the output compiles and runs:
    ```bash
    python src/scraper.py
    ```
*   Verify that `scraper/data/animals.json` contains a valid JSON array of 516 records.
*   Verify that `scraper/images/placeholder.jpg` exists.

### Manual Verification
*   Inspect a subset of the generated `animals.json` to verify that fields (`scientific_name`, `family`, `order`, `habitat`, `country`) are properly mapped and populated.
*   Run the website dev server to confirm that the new dataset loads correctly, and the search and filter functions operate correctly:
    ```bash
    cd website
    npm run dev
    ```
