from html.parser import HTMLParser

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attrs_dict = dict(attrs)
            if "href" in attrs_dict:
                self.links.append((attrs_dict["href"], attrs_dict.get("title", "")))

with open("C:/Users/Guilherme/.gemini/antigravity/brain/dfe1eb06-5940-4b05-80d0-b157521e1600/scratch/search_result.html", "r", encoding="utf-8") as f:
    html = f.read()

parser = LinkParser()
parser.feed(html)

page_links = [l for l in parser.links if "d-16544-p" in l[0]]
print(f"Found {len(page_links)} pagination links:")
for l in page_links[:20]:
    print(f"  {l[0][:100]}... title='{l[1]}'")
if len(page_links) > 20:
    print(f"  ... and {len(page_links) - 20} more")
