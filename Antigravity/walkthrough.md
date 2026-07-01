# Walkthrough — Collembola Scraper Implementation

I have successfully developed and executed the Collembola (springtail) web scraper. The script leverages the official REST API of the **Catálogo Taxonômico da Fauna do Brasil (CTFB)** at `fauna.jbrj.gov.br` to query and process species information.

## Changes Made

### 1. Scraper Implementation
*   **[scraper.py](file:///c:/Users/Guilherme/Documents/GitHub/collembola-project/scraper/src/scraper.py):** Replaced the skeleton code with a fully-functional scraper that:
    *   Queries the official REST view `/v_taxonomia_hierarquia` to fetch all 516 accepted species of the class `Collembola`.
    *   Performs chunked batch requests (50 IDs per batch) to `/v_forma_de_vida_e_substrato` and `/v_distribuicao` to retrieve environments and distribution locations (states).
    *   Maps Portuguese terms (e.g., `TERRESTRE` -> `Terrestrial`) and state codes (e.g., `BR-AM` -> `Amazonas`) to standard readable English fields.
    *   Generates a detailed, descriptive field for each species, dynamically listing its taxonomy, native status, habitat, and occurrence states.
    *   Queries public image endpoints (`ResultadoDaConsultaRecuperandoImagemCampo` and `ResultadoDaConsultaRecuperandoImagemReferencia`) to check for available species images. If images exist, it downloads them; otherwise, it falls back to the default placeholder image.
    *   Outputs the processed records to the target database [animals.json](file:///c:/Users/Guilherme/Documents/GitHub/collembola-project/scraper/data/animals.json).

### 2. High-Quality Placeholder Image
*   **[placeholder.jpg](file:///c:/Users/Guilherme/Documents/GitHub/collembola-project/scraper/images/placeholder.jpg):** Since the CTFB database does not contain images for Collembola species, we used AI generation to produce a premium, modern dark-themed scientific illustration of a springtail. This ensures the data contract rules are satisfied (every referenced image must exist under `images/` and string fields must be non-empty).

---

## Verification Results

### 1. Scraper Output
Running `python src/scraper.py` succeeded and outputted:
*   **Total species processed:** 516
*   **Output file:** [animals.json](file:///c:/Users/Guilherme/Documents/GitHub/collembola-project/scraper/data/animals.json)
*   **Sample data record:**
    ```json
    {
      "id": "jbrj-22462",
      "scientific_name": "Sphaeridia fibulifera",
      "common_name": "Springtail",
      "family": "Sminthurididae",
      "order": "Symphypleona",
      "class": "Collembola",
      "continent": "South America",
      "country": "Brazil (Amazonas)",
      "habitat": "Terrestrial",
      "conservation_status": "NE",
      "description": "A species of springtail in the family Sminthurididae (order Symphypleona). These Collembola are native to Brazil, known to occur in Amazonas, and typically found in terrestrial habitats.",
      "image": "images/placeholder.jpg"
    }
    ```

### 2. Website Integration
*   Copied the generated JSON and images into the `website/public/` folder.
*   Ran `npm install` and compiled the production build with `npm run build` which succeeded in `191ms` with 0 lint errors and warnings.
*   Verified that the public database `website/public/data/animals.json` contains all 516 records, and the placeholder image exists.
