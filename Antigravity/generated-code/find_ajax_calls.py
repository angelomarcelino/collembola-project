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
        
        # Search for any script tags and look for any mentions of "recuperandoImagem" (case insensitive)
        scripts = re.findall(r'<script.*?>((?:.|\n)*?)</script>', html)
        for idx, script in enumerate(scripts):
            if "recuperando" in script.lower():
                print(f"\n--- Script {idx} has matches ---")
                # print lines containing "recuperando" and surrounding 3 lines
                lines = script.splitlines()
                for l_idx, line in enumerate(lines):
                    if "recuperando" in line.lower() or "imagem" in line.lower():
                        start = max(0, l_idx-3)
                        end = min(len(lines), l_idx+4)
                        print(f"Match on line {l_idx}: {line.strip()}")
                        print("Context:")
                        for j in range(start, end):
                            print(f"  {j}: {lines[j].strip()}")
                        print("-" * 20)
except Exception as e:
    print("Error:", e)
