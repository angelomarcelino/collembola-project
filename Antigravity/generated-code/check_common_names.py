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
        print("TIDs:", tids)
        
        # Now query vernacular names for these TIDs
        tids_str = ",".join(map(str, tids))
        url_vn = f"https://fauna.jbrj.gov.br/rest/v_nomes_vernaculares?taxonid=in.({tids_str})"
        print("Querying vernacular names:", url_vn)
        req_vn = urllib.request.Request(url_vn, headers=headers)
        with urllib.request.urlopen(req_vn) as response_vn:
            vn = json.loads(response_vn.read().decode('utf-8'))
            print("Vernacular names found:", vn)
except Exception as e:
    print("Error:", e)
