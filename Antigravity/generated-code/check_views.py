import urllib.request
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

url = "https://fauna.jbrj.gov.br/rest/"
print(f"Querying root: {url}")
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        # PostgREST root usually returns OpenAPI description
        data = json.loads(response.read().decode('utf-8'))
        print("Root response type:", type(data).__name__)
        if isinstance(data, dict):
            print("Keys in root response:", list(data.keys()))
            if "paths" in data:
                print("Available endpoints (first 40):")
                for path in list(data["paths"].keys())[:40]:
                    print(f"  {path}")
                if len(data["paths"]) > 40:
                    print(f"  ... and {len(data['paths']) - 40} more endpoints")
            if "definitions" in data:
                print("Definitions (first 20):", list(data["definitions"].keys())[:20])
except Exception as e:
    print("Error:", e)
