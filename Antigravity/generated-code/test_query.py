import urllib.request
import urllib.parse
import http.cookiejar

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
urllib.request.install_opener(opener)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# 1. Access the main page to establish session
print("Accessing main page...")
req_main = urllib.request.Request(
    "https://fauna.jbrj.gov.br/fauna/listaBrasil/ConsultaPublicaUC/ConsultaPublicaUC.do",
    headers=headers
)
with urllib.request.urlopen(req_main) as response:
    html_main = response.read().decode('utf-8', errors='ignore')
print("Session cookies set:")
for cookie in cookie_jar:
    print(f"  {cookie.name}={cookie.value}")

# 2. Perform search
params = {
    'invalidatePageControlCounter': '1',
    'lingua': '',
    'jsonRank': '',
    'nomeCompleto': '',
    'autor': '',
    'nomeVernaculo': '',
    'rankTaxon': 'CLASSE',
    'nomeTaxon': 'Collembola',
    'formaVida': 'QUALQUER',
    'substrato': 'QUALQUER',
    'ocorrencia': 'OCORRE',
    'regiao': 'QUALQUER',
    'estado': 'QUALQUER',
    'endemismo': 'TODOS',
    'origem': 'TODOS',
    'mostrarAte': 'ESPECIE',  # let's try searching species
    'opcoesBusca': 'NOME_ACEITO'
}

query_string = urllib.parse.urlencode(params)
search_url = f"https://fauna.jbrj.gov.br/fauna/listaBrasil/ConsultaPublicaUC/BemVindoConsultaPublicaConsultar.do?{query_string}"

print(f"Searching: {search_url}")
req_search = urllib.request.Request(search_url, headers=headers)
try:
    with urllib.request.urlopen(req_search) as response:
        # Check if we were redirected
        print(f"Response URL: {response.geturl()}")
        html_search = response.read().decode('utf-8', errors='ignore')
        print(f"Response length: {len(html_search)} characters")
        
        # Let's save a snippet or check for some words
        print("Checking for Collembola in output...")
        print("Number of times 'Collembola' appears:", html_search.lower().count('collembola'))
        
        # Save to file to inspect
        with open("C:\\Users\\Guilherme\\.gemini\\antigravity\\brain\\dfe1eb06-5940-4b05-80d0-b157521e1600\\scratch\\search_result.html", "w", encoding="utf-8") as f:
            f.write(html_search)
        print("Saved to search_result.html")
except Exception as e:
    print("Error:", e)
