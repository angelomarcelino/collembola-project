import urllib.request
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# First, get Collembola species IDs
url_species = "https://fauna.jbrj.gov.br/rest/v_taxonomia_hierarquia?class=eq.Collembola&taxonRank=eq.species&limit=20"
req_species = urllib.request.Request(url_species, headers=headers)
try:
    with urllib.request.urlopen(req_species) as response:
        species = json.loads(response.read().decode('utf-8'))
        tids = [item['taxonID'] for item in species]
        
        # Query life form and substrate
        tids_str = ",".join(map(str, tids))
        url_hab = f"https://fauna.jbrj.gov.br/rest/v_forma_de_vida_e_substrato?taxonid=in.({tids_str})"
        req_hab = urllib.request.Request(url_hab, headers=headers)
        with urllib.request.urlopen(req_hab) as response_hab:
            habs = json.loads(response_hab_read := response_hab.read().decode('utf-8'))
            print("Habitats found:")
            for item in habs[:20]:
                print(item)
except Exception as e:
    print("Error:", e)
