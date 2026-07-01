import urllib.request
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

url = "https://fauna.jbrj.gov.br/rest/v_taxon_data?idtaxon_pai=in.(448,438)"
print(f"Querying: {url}")
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
        print("Response count:", len(data))
        for item in data[:5]:
            print(f"  {item['nome']} (rank: {item['rank']}, parent: {item['idtaxon_pai']})")
except Exception as e:
    print("Error:", e)
