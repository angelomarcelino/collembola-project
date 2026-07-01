import urllib.request
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

url = "https://fauna.jbrj.gov.br/fauna/faunadobrasil/22462"
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8', errors='ignore')
        
        # Look for $.ajax calls
        ajax_calls = re.findall(r'\$\.ajax\(\{((?:.|\n)*?)\}\)', html)
        print(f"Found {len(ajax_calls)} $.ajax calls:")
        for idx, call in enumerate(ajax_calls):
            print(f"\n--- Ajax Call {idx} ---")
            print(call.strip()[:1000]) # show first 1000 chars of each ajax call
except Exception as e:
    print("Error:", e)
