import urllib.request
from html.parser import HTMLParser

class SelectParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current_select = None
        self.selects = {}

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "select":
            self.current_select = attrs_dict.get("name", "unnamed")
            self.selects[self.current_select] = []
        elif tag == "option" and self.current_select:
            self.selects[self.current_select].append({
                "value": attrs_dict.get("value", ""),
                "selected": "selected" in attrs_dict,
                "text": ""
            })

    def handle_data(self, data):
        if self.current_select and self.selects[self.current_select]:
            self.selects[self.current_select][-1]["text"] += data.strip()

    def handle_endtag(self, tag):
        if tag == "select":
            self.current_select = None

url = "https://fauna.jbrj.gov.br/fauna/listaBrasil/ConsultaPublicaUC/ConsultaPublicaUC.do"
try:
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8', errors='ignore')
    
    parser = SelectParser()
    parser.feed(html)
    
    for select_name, options in parser.selects.items():
        print(f"Select: {select_name}")
        for opt in options[:20]: # show first 20 options
            print(f"  value='{opt['value']}' text='{opt['text']}'{' [selected]' if opt['selected'] else ''}")
        if len(options) > 20:
            print(f"  ... and {len(options) - 20} more options")
except Exception as e:
    print("Error:", e)
