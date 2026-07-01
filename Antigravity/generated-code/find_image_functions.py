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
        
        # Look for function definitions in inline scripts
        scripts = re.findall(r'<script.*?>((?:.|\n)*?)</script>', html)
        print(f"Total script blocks: {len(scripts)}")
        for idx, script in enumerate(scripts):
            functions = re.findall(r'function\s+(\w+)\s*\(', script)
            if functions:
                print(f"Script {idx} defines functions: {functions}")
                # check if any function name mentions image or load or carry
                for fn in functions:
                    if any(k in fn.lower() for k in ["imagem", "image", "carrega", "load", "recupera", "fsi", "inct"]):
                        print(f"  -> Match in Script {idx} for function '{fn}'")
                        # print the function body (rough estimate)
                        fn_match = re.search(r'function\s+' + fn + r'\b((?:.|\n)*?)(?=function\s+|\Z)', script)
                        if fn_match:
                            print(f"  Body snippet:\n{fn_match.group(0)[:1500]}")
except Exception as e:
    print("Error:", e)
