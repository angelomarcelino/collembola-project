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
        
        # Find custom elements (tags containing a hyphen)
        tags = re.findall(r'<([a-zA-Z]+-[a-zA-Z0-9-]+)\b', html)
        print("Custom tags found:", set(tags))
        
        # Find all script src paths
        scripts = re.findall(r'<script\s+[^>]*src=["\'](.*?)["\']', html)
        print("Script sources:")
        for src in scripts:
            print(f"  {src}")
except Exception as e:
    print("Error:", e)
