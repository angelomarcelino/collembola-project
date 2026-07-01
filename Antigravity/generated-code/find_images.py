import urllib.request
import json
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# 1. Fetch species from API
url_species = "https://fauna.jbrj.gov.br/rest/v_taxonomia_hierarquia?class=eq.Collembola&taxonRank=eq.species&taxonomicStatus=eq.accepted"
req = urllib.request.Request(url_species, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        species_list = json.loads(response.read().decode('utf-8'))
except Exception as e:
    print("Failed to fetch species list:", e)
    species_list = []

print(f"Total species to check: {len(species_list)}")

found = 0
for idx, sp in enumerate(species_list):
    tid = sp['taxonID']
    name = sp['scientificName']
    
    url_campo = f"https://fauna.jbrj.gov.br/fauna/listaBrasil/ConsultaPublicaUC/ResultadoDaConsultaRecuperandoImagemCampo.do?idTaxon={tid}"
    url_ref = f"https://fauna.jbrj.gov.br/fauna/listaBrasil/ConsultaPublicaUC/ResultadoDaConsultaRecuperandoImagemReferencia.do?idTaxon={tid}"
    
    # Check ImagemCampo
    try:
        req = urllib.request.Request(url_campo, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get('imagensCampos'):
                print(f"[{idx}/{len(species_list)}] Species {name} (ID: {tid}) HAS FIELD IMAGES:")
                print(data['imagensCampos'])
                found += 1
    except Exception as e:
        pass # Ignore individual errors
        
    # Check ImagemReferencia
    try:
        req = urllib.request.Request(url_ref, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get('ImagemReferencia'):
                print(f"[{idx}/{len(species_list)}] Species {name} (ID: {tid}) HAS REFERENCE IMAGES:")
                print(data['ImagemReferencia'])
                found += 1
    except Exception as e:
        pass # Ignore individual errors
        
    if found >= 5:
        print("Found enough examples.")
        break
        
    time.sleep(0.05) # small sleep
