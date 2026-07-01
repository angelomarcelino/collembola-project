import urllib.request
from html.parser import HTMLParser

class ImageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            attrs_dict = dict(attrs)
            self.images.append(attrs_dict)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Let's check a few species pages.
# Let's try species ID 22462 (Sphaeridia fibulifera)
url = "https://fauna.jbrj.gov.br/fauna/faunadobrasil/22462"
print(f"Querying page: {url}")
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8', errors='ignore')
        parser = ImageParser()
        parser.feed(html)
        print("Images found on page:")
        for img in parser.images:
            print(f"  src='{img.get('src')}', class='{img.get('class')}', id='{img.get('id')}'")
except Exception as e:
    print("Error:", e)
