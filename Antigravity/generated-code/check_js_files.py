import urllib.request

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

js_files = [
    "layout-common.js",
    "scripts.js",
    "jquery.displaytag-ajax-1.2-mdarte.js"
]

for filename in js_files:
    url = f"https://fauna.jbrj.gov.br/fauna/layout/default/javaScripts/{filename}"
    print(f"\n--- Checking: {url} ---")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8', errors='ignore')
            print(f"Loaded {len(content)} characters")
            # Search for Recuperando or Imagem
            for term in ["Recuperando", "Imagem", "ajax-loader", "load", "post", "get"]:
                count = content.lower().count(term.lower())
                print(f"  '{term}': {count} occurrences")
            # Let's search for some patterns
            lines = content.splitlines()
            for idx, line in enumerate(lines):
                if "recuperando" in line.lower() or "imagem" in line.lower():
                    if len(line.strip()) < 500:
                        print(f"  Line {idx}: {line.strip()}")
    except Exception as e:
        print("Error:", e)
