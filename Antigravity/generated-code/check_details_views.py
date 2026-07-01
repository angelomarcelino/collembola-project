import urllib.request
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

views = [
    'v_distribuicao',
    'v_forma_de_vida_e_substrato',
    'v_nomes_vernaculares',
    'v_taxonomia_hierarquia'
]

for view in views:
    url = f"https://fauna.jbrj.gov.br/rest/{view}?limit=1"
    print(f"\n--- Fields in {view} ---")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            if isinstance(data, list) and len(data) > 0:
                for k, v in data[0].items():
                    print(f"  {k}: {type(v).__name__} = {v}")
            else:
                print("Empty or not list response:", data)
    except Exception as e:
        print("Error:", e)
