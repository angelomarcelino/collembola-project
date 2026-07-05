"""Main scraper module for extracting Collembola species data."""

import json
import logging
import urllib.request
import urllib.parse
import time
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
DATA_DIR = Path(__file__).parent.parent / "data"
IMAGES_DIR = Path(__file__).parent.parent / "images"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

STATES_MAP = {
    'AC': 'Acre', 'AL': 'Alagoas', 'AP': 'Amapá', 'AM': 'Amazonas',
    'BA': 'Bahia', 'CE': 'Ceará', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo',
    'GO': 'Goiás', 'MA': 'Maranhão', 'MT': 'Mato Grosso', 'MS': 'Mato Grosso do Sul',
    'MG': 'Minas Gerais', 'PA': 'Pará', 'PB': 'Paraíba', 'PR': 'Paraná',
    'PE': 'Pernambuco', 'PI': 'Piauí', 'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte',
    'RS': 'Rio Grande do Sul', 'RO': 'Rondônia', 'RR': 'Roraima', 'SC': 'Santa Catarina',
    'SP': 'São Paulo', 'SE': 'Sergipe', 'TO': 'Tocantins'
}

HABITAT_MAP = {
    'TERRESTRE': 'Terrestre',
    'AGUA_DOCE': 'Água Doce',
    'MARINHO': 'Marinho',
    'AGUAS_SUBTERRANEAS': 'Águas Subterrâneas',
    'CAVERNICOLA': 'Cavernícola',
    'FOSSORIAL': 'Fossorial',
    'ARBOREO': 'Arbóreo',
}

def query_api(endpoint):
    """Query a REST endpoint on the fauna.jbrj.gov.br server."""
    url = f"https://fauna.jbrj.gov.br/rest/{endpoint}"
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            logger.warning(f"Error querying {url} (attempt {attempt+1}/3): {e}")
            time.sleep(1)
    return []

def query_url(url):
    """Query a general URL on the JBRJ server returning JSON."""
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            logger.warning(f"Error calling {url} (attempt {attempt+1}/3): {e}")
            time.sleep(1)
    return None

def download_image(img_url, dest_path):
    """Download an image from a URL and save it to the destination path."""
    req = urllib.request.Request(img_url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(dest_path, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        logger.error(f"Failed to download image from {img_url}: {e}")
        return False

def batch_query(endpoint_template, ids, batch_size=50):
    """Perform queries in batches to avoid URL size limitations."""
    results = []
    for i in range(0, len(ids), batch_size):
        chunk = ids[i:i+batch_size]
        ids_str = ",".join(map(str, chunk))
        query = endpoint_template.format(ids_str)
        chunk_results = query_api(query)
        if chunk_results:
            results.extend(chunk_results)
        time.sleep(0.05)
    return results

def scrape():
    """Main scraping function to extract Collembola species data."""
    logger.info("Starting Collembola species data scraping from fauna.jbrj.gov.br...")

    # 1. Fetch all accepted Collembola species
    logger.info("Fetching accepted Collembola species from v_taxonomia_hierarquia...")
    species_list = query_api("v_taxonomia_hierarquia?class=eq.Collembola&taxonRank=eq.species&taxonomicStatus=eq.accepted")
    
    if not species_list:
        logger.error("No species retrieved. Aborting.")
        return

    logger.info(f"Retrieved {len(species_list)} accepted species.")

    # Get unique taxon IDs
    taxon_ids = [int(sp['taxonID']) for sp in species_list]

    # 2. Fetch habitats in batch
    logger.info("Fetching habitats from v_forma_de_vida_e_substrato in batches...")
    habitats_raw = batch_query("v_forma_de_vida_e_substrato?taxonid=in.({0})", taxon_ids)
    
    # Map habitats by taxon ID
    habitats_by_taxon = {}
    for h in habitats_raw:
        tid = h.get('taxonid')
        hab_val = h.get('habitat')
        if tid and hab_val:
            mapped_hab = HABITAT_MAP.get(hab_val, hab_val.capitalize())
            habitats_by_taxon.setdefault(tid, set()).add(mapped_hab)

    # 3. Fetch distributions in batch
    logger.info("Fetching distributions from v_distribuicao in batches...")
    distributions_raw = batch_query("v_distribuicao?taxonID=in.({0})", taxon_ids)

    # Map distributions by taxon ID
    distributions_by_taxon = {}
    for d in distributions_raw:
        tid = d.get('taxonID')
        loc_id = d.get('locationID', '')
        if tid and loc_id.startswith('BR-'):
            state_code = loc_id.replace('BR-', '')
            state_name = STATES_MAP.get(state_code, state_code)
            distributions_by_taxon.setdefault(tid, set()).add(state_name)

    # 4. Load overrides
    overrides_file = DATA_DIR / "image_overrides.json"
    overrides_dict = {}
    if overrides_file.exists():
        with open(overrides_file, 'r', encoding='utf-8') as f:
            overrides_dict = json.load(f)
            
    # 5. Process each species and fetch images
    processed_animals = []
    
    for idx, sp in enumerate(species_list):
        tid = int(sp['taxonID'])
        scientific_name_full = sp['scientificName']
        
        # Build binomial name from Genus + specificEpithet
        genus = sp.get('genus', '')
        epithet = sp.get('specificEpithet', '')
        infra_epithet = sp.get('infraspecificEpithet', '')
        
        if genus and epithet:
            scientific_name = f"{genus} {epithet}"
            if infra_epithet:
                scientific_name += f" {infra_epithet}"
        else:
            # Fallback to splitting scientificName and dropping author details
            scientific_name = scientific_name_full.split(' ')[0]
            if len(scientific_name_full.split(' ')) > 1:
                scientific_name += ' ' + scientific_name_full.split(' ')[1]

        family = sp.get('family', 'Unknown Family')
        order = sp.get('subOrder', 'Collembola')
        if not order:
            order = 'Collembola'

        # Get unique habitats
        habs = list(habitats_by_taxon.get(tid, ["Terrestrial"]))
        habitat = ", ".join(sorted(habs))

        # Get unique states
        states = list(distributions_by_taxon.get(tid, []))
        if states:
            states_str = ", ".join(sorted(states))
            country = f"Brazil ({states_str})"
        else:
            country = "Brazil"

        # Check for images on JBRJ endpoints
        img_filename = f"{tid}.jpg"
        img_dest_path = IMAGES_DIR / img_filename
        image_path = f"images/placeholder.jpg" # Default placeholder

        downloaded = False
        
        # Check for manual overrides first
        override_img = overrides_dict.get(scientific_name)
        if override_img:
            if override_img.startswith("http"):
                logger.info(f"Downloading OVERRIDE image for {scientific_name}: {override_img}")
                downloaded = download_image(override_img, img_dest_path)
            else:
                logger.info(f"Using OVERRIDE path for {scientific_name}: {override_img}")
                image_path = override_img
                downloaded = True

        if not downloaded:
            # Query iNaturalist observations with research grade
            url_inat = f"https://api.inaturalist.org/v1/observations?taxon_name={urllib.parse.quote(scientific_name)}&quality_grade=research&has[]=photos&per_page=1"
            inat_data = query_url(url_inat)
            if inat_data and inat_data.get('results'):
                result = inat_data['results'][0]
                if result.get('photos') and len(result['photos']) > 0:
                    img_url = result['photos'][0]['url'].replace('square', 'medium')
                    logger.info(f"Downloading iNaturalist Research Grade image for {scientific_name}: {img_url}")
                    downloaded = download_image(img_url, img_dest_path)
            
            # Fallback to iNaturalist Taxa (default photo) if no research grade observations exist
            if not downloaded:
                url_inat_taxa = f"https://api.inaturalist.org/v1/taxa?q={urllib.parse.quote(scientific_name)}&per_page=1"
                inat_taxa_data = query_url(url_inat_taxa)
                if inat_taxa_data and inat_taxa_data.get('results'):
                    result = inat_taxa_data['results'][0]
                    if result.get('default_photo') and result['default_photo'].get('medium_url'):
                        img_url = result['default_photo']['medium_url']
                        logger.info(f"Downloading iNaturalist Taxa image for {scientific_name}: {img_url}")
                        downloaded = download_image(img_url, img_dest_path)

        # Fallback to iNaturalist if JBRJ fails or has no images
        if not downloaded:
            url_inat = f"https://api.inaturalist.org/v1/taxa?q={urllib.parse.quote(scientific_name)}&per_page=1"
            inat_data = query_url(url_inat)
            if inat_data and inat_data.get('results'):
                result = inat_data['results'][0]
                if result.get('default_photo') and result['default_photo'].get('medium_url'):
                    img_url = result['default_photo']['medium_url']
                    logger.info(f"Downloading iNaturalist image for {scientific_name}: {img_url}")
                    downloaded = download_image(img_url, img_dest_path)

        # Fallback to GBIF if not downloaded yet
        if not downloaded:
            url_gbif = f"https://api.gbif.org/v1/occurrence/search?scientificName={urllib.parse.quote(scientific_name)}&mediaType=StillImage&limit=1&basisOfRecord=HUMAN_OBSERVATION"
            gbif_data = query_url(url_gbif)
            if gbif_data and gbif_data.get('results'):
                result = gbif_data['results'][0]
                if result.get('media'):
                    images = [m for m in result['media'] if m.get('type') == 'StillImage']
                    if images and images[0].get('identifier'):
                        img_url = images[0]['identifier']
                        logger.info(f"Downloading GBIF image for {scientific_name}: {img_url}")
                        downloaded = download_image(img_url, img_dest_path)

        if downloaded:
            image_path = f"images/{img_filename}"

        # Construct description
        desc_states = f"ocorrer em: {states_str}" if states else "ocorrer no Brasil"
        description = (
            f"Uma espécie de colêmbolo da família {family} (ordem {order}). "
            f"Estes pequenos artrópodes são nativos do Brasil, conhecidos por {desc_states}, "
            f"e tipicamente encontrados em habitats do tipo {habitat.lower()}."
        )

        animal = {
            "id": f"jbrj-{tid}",
            "scientific_name": scientific_name,
            "common_name": "Colêmbolo",
            "family": family,
            "order": order,
            "class": "Collembola",
            "continent": "América do Sul",
            "country": country,
            "habitat": habitat,
            "conservation_status": "NE", # Not Evaluated (default)
            "description": description,
            "image": image_path
        }
        
        processed_animals.append(animal)
        
        if (idx + 1) % 50 == 0 or (idx + 1) == len(species_list):
            logger.info(f"Processed {idx + 1}/{len(species_list)} species...")

    # 5. Output animals.json
    output_file = DATA_DIR / "animals.json"
    logger.info(f"Writing {len(processed_animals)} records to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_animals, f, ensure_ascii=False, indent=2)

    # 6. Enrich data with JBRJ mv_planilha_extendida
    logger.info("Enriching data with JBRJ mv_planilha_extendida...")
    try:
        import urllib.request
        req = urllib.request.Request("https://fauna.jbrj.gov.br/rest/mv_planilha_extendida?class=eq.Collembola", headers=HEADERS)
        with urllib.request.urlopen(req) as response:
            rich_data_list = json.loads(response.read().decode('utf-8'))
        
        rich_map = {str(item.get("taxonID")): item for item in rich_data_list if item.get("taxonID")}
        
        for animal in processed_animals:
            tid = animal["id"].replace("jbrj-", "")
            rich_info = rich_map.get(tid)
            if not rich_info: continue
            
            is_endemic = rich_info.get("endemicBrazil") == "SIM"
            origin = rich_info.get("establishmentMeans", "")
            environments = rich_info.get("environment", "")
            
            base_desc = animal.get("description", "")
            if base_desc.endswith("."): base_desc = base_desc[:-1]
            
            rich_parts = []
            if is_endemic: rich_parts.append("É uma espécie endêmica do Brasil (exclusiva do nosso território)")
            elif origin.lower() == "native": rich_parts.append("É uma espécie nativa do Brasil")
            elif origin.lower() == "introduced": rich_parts.append("É uma espécie introduzida no Brasil (exótica)")
            
            if environments:
                envs = [e.strip().capitalize() for e in environments.split(",")]
                rich_parts.append(f"associada a ambientes {' e '.join(envs).lower()}")
                
            if rich_parts:
                animal["description"] = base_desc + ". " + ", ".join(rich_parts).capitalize() + "."
            
            biblio = rich_info.get("bibliographicReference", "").strip()
            if biblio:
                animal["bibliography"] = biblio
                
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_animals, f, ensure_ascii=False, indent=2)
        logger.info("Enrichment complete.")
    except Exception as e:
        logger.error(f"Failed to enrich data: {e}")
        
    logger.info("Scraping completed successfully!")

if __name__ == "__main__":
    scrape()

