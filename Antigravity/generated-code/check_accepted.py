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
        statuses = set(item.get('taxonomicStatus') for item in data)
        print("Unique taxonomicStatus values:", statuses)
        # Let's count each status
        counts = {}
        for item in data:
            st = item.get('taxonomicStatus')
            counts[st] = counts.get(st, 0) + 1
        print("Counts by status:", counts)
except Exception as e:
    print("Error:", e)
