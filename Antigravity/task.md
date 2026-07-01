# Tasks — Develop Collembola Scraper

- [x] Generate a premium placeholder image for springtails and save to `scraper/images/placeholder.jpg`
- [x] Implement the scraper code in `scraper/src/scraper.py`
  - [x] Fetch accepted species from `/v_taxonomia_hierarquia`
  - [x] Fetch habitats from `/v_forma_de_vida_e_substrato` (batch requests)
  - [x] Fetch distributions from `/v_distribuicao` (batch requests)
  - [x] Map Portuguese terms to English and format fields according to the data contract
  - [x] Aggregate occurrences into the `country` field
  - [x] Save the final list to `scraper/data/animals.json`
- [x] Run and verify the scraper output
- [x] Build and verify the React frontend with the new data
