import urllib.request
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Get Collembola species IDs
url_species = "https://fauna.jbrj.gov.br/rest/v_taxonomia_hierarquia?class=eq.Collembola&taxonRank=eq.species&limit=20"
req_species = urllib.request.Request(url_species, headers=headers)
try:
    with urllib.request.urlopen(req_species) as response:
        species = json.loads(response.read().decode('utf-8'))
        tids = [item['taxonID'] for item in species]
        
        # Query distribution
        tids_str = ",".join(map(str, tids))
        url_dist = f"https://fauna.jbrj.gov.br/rest/v_distribuicao?taxonID=in.({tids_str})"
        req_dist = urllib.request.Request(url_dist, headers=headers)
        with urllib.request.urlopen(req_dist) as response_dist:
            dists = json.loads(response_dist.read().decode('utf-8'))
            print("Distribution records:")
            for item in dists[:20]:
                print(item)
except Exception as e:
    print("Error:", e)
