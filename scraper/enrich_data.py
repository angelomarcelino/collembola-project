import json
import urllib.request

print("Fetching rich data from JBRJ mv_planilha_extendida...")
req = urllib.request.Request("https://fauna.jbrj.gov.br/rest/mv_planilha_extendida?class=eq.Collembola", headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    rich_data_list = json.loads(response.read().decode('utf-8'))

rich_map = {}
for item in rich_data_list:
    tid = item.get("taxonID")
    if tid:
        rich_map[f"jbrj-{tid}"] = item

files_to_enrich = ["../scraper/data/animals.json"]

for file_path in files_to_enrich:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            animals = json.load(f)
            
        for animal in animals:
            tid = animal["id"]
            rich_info = rich_map.get(tid)
            if not rich_info:
                continue
                
            # Extract rich fields
            is_endemic = rich_info.get("endemicBrazil") == "SIM"
            origin = rich_info.get("establishmentMeans", "")
            environments = rich_info.get("environment", "")
            
            # Start building rich description
            base_desc = animal.get("description", "")
            
            # Remove the last period to append more
            if base_desc.endswith("."):
                base_desc = base_desc[:-1]
                
            rich_parts = []
            
            if is_endemic:
                rich_parts.append("É uma espécie endêmica do Brasil (exclusiva do nosso território)")
            elif origin.lower() == "native":
                rich_parts.append("É uma espécie nativa do Brasil")
            elif origin.lower() == "introduced":
                rich_parts.append("É uma espécie introduzida no Brasil (exótica)")
                
            if environments:
                # environments is usually "EPICONTINENTAL", "MARINHO", etc.
                envs = [e.strip().capitalize() for e in environments.split(",")]
                rich_parts.append(f"associada a ambientes {' e '.join(envs).lower()}")
                
            if rich_parts:
                rich_addition = ". " + ", ".join(rich_parts).capitalize() + "."
                animal["description"] = base_desc + rich_addition
                
            # Add bibliography to the animal object if it exists
            biblio = rich_info.get("bibliographicReference", "").strip()
            if biblio:
                animal["bibliography"] = biblio

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(animals, f, ensure_ascii=False, indent=2)
            
        print(f"Enriched {len(animals)} records in {file_path}")
    except Exception as e:
        print(f"Could not enrich {file_path}: {e}")
