import json

files = ["../scraper/data/animals.json"]

for file_path in files:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        for animal in data:
            # Common Name
            if animal.get("common_name") in ["Springtail", "Collembola"]:
                animal["common_name"] = "Colêmbolo"
                
            # Continent
            if animal.get("continent") == "South America":
                animal["continent"] = "América do Sul"
                
            # Habitat
            habitat = animal.get("habitat", "")
            habitat_map = {
                'Terrestrial': 'Terrestre',
                'Freshwater': 'Água Doce',
                'Marine': 'Marinho',
                'Subterranean': 'Águas Subterrâneas',
                'Cave/Subterranean': 'Cavernícola',
                'Fossorial': 'Fossorial',
                'Arboreal': 'Arbóreo',
            }
            # Replace English words with Portuguese words
            for eng, pt in habitat_map.items():
                habitat = habitat.replace(eng, pt)
            animal["habitat"] = habitat
            
            # Description
            desc = animal.get("description", "")
            if desc.startswith("A species of springtail in the family "):
                family = animal.get("family", "")
                order = animal.get("order", "")
                
                # Extract the "occur in XXX" part
                states_part = "ocorrer no Brasil"
                if "known to occur in " in desc:
                    states_raw = desc.split("known to occur in ")[1].split(", and")[0]
                    states_part = f"ocorrer em: {states_raw}"
                    
                pt_desc = (
                    f"Uma espécie de colêmbolo da família {family} (ordem {order}). "
                    f"Estes pequenos artrópodes são nativos do Brasil, conhecidos por {states_part}, "
                    f"e tipicamente encontrados em habitats do tipo {habitat.lower()}."
                )
                animal["description"] = pt_desc

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"Translated {len(data)} records in {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
