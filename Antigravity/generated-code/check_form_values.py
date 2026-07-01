from html.parser import HTMLParser

class FormParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_form = False
        self.inputs = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "form":
            self.in_form = True
        elif self.in_form and tag in ("input", "select"):
            self.inputs.append((tag, attrs_dict.get("name"), attrs_dict.get("value")))

    def handle_endtag(self, tag):
        if tag == "form":
            self.in_form = False

filepath = "C:/Users/Guilherme/.gemini/antigravity/brain/dfe1eb06-5940-4b05-80d0-b157521e1600/scratch/search_result.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

parser = FormParser()
parser.feed(html)

print("All Form inputs:")
for tag, name, val in parser.inputs:
    print(f"  {tag}: name={name}, value={val}")
