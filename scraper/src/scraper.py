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
    'TERRESTRE': 'Terrestrial',
    'AGUA_DOCE': 'Freshwater',
    'MARINHO': 'Marine',
    'AGUAS_SUBTERRANEAS': 'Subterranean',
    'CAVERNICOLA': 'Cave/Subterranean',
    'FOSSORIAL': 'Fossorial',
    'ARBOREO': 'Arboreal',
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

    # 4. Process each species and fetch images
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

        # Check field images
        url_campo = f"https://fauna.jbrj.gov.br/fauna/listaBrasil/ConsultaPublicaUC/ResultadoDaConsultaRecuperandoImagemCampo.do?idTaxon={tid}"
        campo_data = query_url(url_campo)
        downloaded = False
        
        if campo_data and campo_data.get('imagensCampos'):
            img_info = campo_data['imagensCampos'][0]
            # Try urlImageRealSize first, fallback to urlImageReducedSize
            img_url = img_info.get('urlImageRealSize') or img_info.get('urlImageReducedSize')
            if img_url:
                if img_url.startswith('/'):
                    img_url = "https://fauna.jbrj.gov.br" + img_url
                logger.info(f"Downloading field image for {scientific_name}: {img_url}")
                downloaded = download_image(img_url, img_dest_path)

        # Check reference images if field images not available
        if not downloaded:
            url_ref = f"https://fauna.jbrj.gov.br/fauna/listaBrasil/ConsultaPublicaUC/ResultadoDaConsultaRecuperandoImagemReferencia.do?idTaxon={tid}"
            ref_data = query_url(url_ref)
            if ref_data and ref_data.get('ImagemReferencia'):
                img_info = ref_data['ImagemReferencia'][0]
                img_url = img_info.get('caminhoCompletoImagem')
                if img_url:
                    if img_url.startswith('/'):
                        img_url = "https://fauna.jbrj.gov.br" + img_url
                    logger.info(f"Downloading reference image for {scientific_name}: {img_url}")
                    downloaded = download_image(img_url, img_dest_path)

        if downloaded:
            image_path = f"images/{img_filename}"

        # Construct description
        desc_states = f"occur in {states_str}" if states else "occur in Brazil"
        description = (
            f"A species of springtail in the family {family} (order {order}). "
            f"These Collembola are native to Brazil, known to {desc_states}, "
            f"and typically found in {habitat.lower()} habitats."
        )

        animal = {
            "id": f"jbrj-{tid}",
            "scientific_name": scientific_name,
            "common_name": "Springtail",
            "family": family,
            "order": order,
            "class": "Collembola",
            "continent": "South America",
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
        
    logger.info("Scraping completed successfully!")

if __name__ == "__main__":
    scrape()

