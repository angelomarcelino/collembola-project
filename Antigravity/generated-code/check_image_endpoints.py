import urllib.request
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

tid = 22462  # Sphaeridia fibulifera

endpoints = [
    ("ImagemCampo", f"https://fauna.jbrj.gov.br/fauna/listaBrasil/ConsultaPublicaUC/ResultadoDaConsultaRecuperandoImagemCampo.do?idTaxon={tid}"),
    ("ImagemReferencia", f"https://fauna.jbrj.gov.br/fauna/listaBrasil/ConsultaPublicaUC/ResultadoDaConsultaRecuperandoImagemReferencia.do?idTaxon={tid}"),
    ("ImagemVoucherINCT", f"https://fauna.jbrj.gov.br/fauna/listaBrasil/ConsultaPublicaUC/ResultadoDaConsultaRecuperandoImagemVoucher.do?idTaxon={tid}&origemTestemunho=INCT"),
    ("ImagemVoucherHV", f"https://fauna.jbrj.gov.br/fauna/listaBrasil/ConsultaPublicaUC/ResultadoDaConsultaRecuperandoImagemVoucher.do?idTaxon={tid}&origemTestemunho=HV")
]

for name, url in endpoints:
    print(f"\n--- Endpoint {name} ---")
    print(f"URL: {url}")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            res_content = response.read().decode('utf-8')
            print(f"Length: {len(res_content)}")
            try:
                data = json.loads(res_content)
                print("JSON Data:", data)
            except Exception as e:
                print("Not valid JSON. Sample output:", res_content[:300])
    except Exception as e:
        print("Error:", e)
