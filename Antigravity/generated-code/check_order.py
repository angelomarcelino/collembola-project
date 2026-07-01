import urllib.request
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

url = "https://fauna.jbrj.gov.br/rest/v_taxonomia_hierarquia?class=eq.Collembola&taxonRank=eq.species&limit=20"
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        species = json.loads(response.read().decode('utf-8'))
        for item in species[:10]:
            print(f"Name: {item['scientificName']}")
            print(f"  order: {item.get('order')}")
            print(f"  subOrder: {item.get('subOrder')}")
            print(f"  family: {item.get('family')}")
except Exception as e:
    print("Error:", e)
