import urllib.request
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
                "id": attrs_dict.get("id", ""),
                "name": attrs_dict.get("name", ""),
                "method": attrs_dict.get("method", "get"),
                "inputs": []
            }
            self.forms.append(self.current_form)
        elif self.in_form and tag in ("input", "select", "textarea"):
            if self.current_form:
                self.current_form["inputs"].append({
                    "tag": tag,
                    "name": attrs_dict.get("name", ""),
                    "type": attrs_dict.get("type", ""),
                    "value": attrs_dict.get("value", "")
                })

    def handle_endtag(self, tag):
        if tag == "form":
            self.in_form = False

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

url = "https://fauna.jbrj.gov.br/fauna/faunadobrasil/22462"
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8', errors='ignore')
        parser = FormParser()
        parser.feed(html)
        print(f"Found {len(parser.forms)} forms:")
        for idx, form in enumerate(parser.forms):
            print(f"\nForm {idx}: action='{form['action']}', id='{form['id']}', name='{form['name']}'")
            for inp in form["inputs"]:
                print(f"  {inp['tag']}: name='{inp['name']}', type='{inp['type']}', value='{inp['value']}'")
except Exception as e:
    print("Error:", e)
