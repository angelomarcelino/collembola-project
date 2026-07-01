import urllib.request
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

url = "https://fauna.jbrj.gov.br/rest/v_taxonomia_hierarquia?class=eq.Collembola&taxonRank=eq.species"
print(f"Querying: {url}")
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
        print("Response count:", len(data))
        if data:
            print("First item keys:", list(data[0].keys()))
            print("First item sample:")
            for k, v in data[0].items():
                if v:
                    print(f"  {k}: {v}")
except Exception as e:
    print("Error:", e)
