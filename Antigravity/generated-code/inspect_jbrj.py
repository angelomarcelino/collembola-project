import urllib.request
import urllib.parse
from html.parser import HTMLParser

class FormParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_form = False
        self.current_form = None
        self.forms = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "form":
            self.in_form = True
            self.current_form = {
                "action": attrs_dict.get("action", ""),
                "method": attrs_dict.get("method", "get").lower(),
                "inputs": []
            }
            self.forms.append(self.current_form)
        elif self.in_form and tag in ("input", "select", "textarea"):
            if self.current_form is not None:
                self.current_form["inputs"].append({
                    "tag": tag,
                    "name": attrs_dict.get("name", ""),
                    "type": attrs_dict.get("type", ""),
                    "value": attrs_dict.get("value", "")
                })

    def handle_endtag(self, tag):
        if tag == "form":
            self.in_form = False

url = "https://fauna.jbrj.gov.br/fauna/listaBrasil/ConsultaPublicaUC/ConsultaPublicaUC.do"
try:
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8', errors='ignore')
    
    parser = FormParser()
    parser.feed(html)
    
    print(f"Found {len(parser.forms)} forms:")
    for i, form in enumerate(parser.forms):
        print(f"\nForm {i}: action='{form['action']}', method='{form['method']}'")
        for inp in form["inputs"]:
            print(f"  {inp['tag']}: name='{inp['name']}', type='{inp['type']}', value='{inp['value']}'")
except Exception as e:
    print("Error:", e)
