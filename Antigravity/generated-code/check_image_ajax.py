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
        
        # Let's search for lines containing $.ajax or ajax or post or get or RecuperandoImagem
        lines = html.splitlines()
        print(f"Total lines: {len(lines)}")
        for idx, line in enumerate(lines):
            if any(k in line for k in ["Recuperando", "Imagem", "ajax", "image", "img"]):
                if len(line.strip()) < 500: # avoid print extremely long lines
                    print(f"Line {idx}: {line.strip()}")
except Exception as e:
    print("Error:", e)
