from html.parser import HTMLParser

class ResultsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.classes = set()
        self.ids = set()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag not in self.tags:
            self.tags.append(tag)
        if "class" in attrs_dict:
            self.classes.update(attrs_dict["class"].split())
        if "id" in attrs_dict:
            self.ids.add(attrs_dict["id"])
        if tag == "a" and "href" in attrs_dict:
            self.links.append((attrs_dict["href"], attrs_dict.get("title", "")))

with open("C:\\Users\\Guilherme\\.gemini\\antigravity\\brain\\dfe1eb06-5940-4b05-80d0-b157521e1600\\scratch\\search_result.html", "r", encoding="utf-8") as f:
    html = f.read()

parser = ResultsParser()
parser.feed(html)

print("Unique HTML Tags:", parser.tags)
print("\nUnique Classes (first 30):", sorted(list(parser.classes))[:30])
print("\nUnique IDs (first 30):", sorted(list(parser.ids))[:30])
print(f"\nTotal links found: {len(parser.links)}")
print("\nSample Links (first 30):")
for link, title in parser.links[:30]:
    print(f"  href='{link}' title='{title}'")
