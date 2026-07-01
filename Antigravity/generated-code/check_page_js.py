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
        
        # Print script tags content or scripts
        scripts = re.findall(r'<script.*?>((?:.|\n)*?)</script>', html)
        print(f"Found {len(scripts)} script blocks:")
        for idx, script in enumerate(scripts):
            if "idImage" in script or "ajax" in script or "Imagem" in script or "image" in script.lower():
                print(f"\n--- Script {idx} ---")
                print(script.strip()[:1000]) # first 1000 chars
except Exception as e:
    print("Error:", e)
