import urllib.request
import urllib.parse
import json

def test_gbif_occurrence(species_name):
    url = f"https://api.gbif.org/v1/occurrence/search?scientificName={urllib.parse.quote(species_name)}&mediaType=StillImage&limit=1"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())
            results = data.get('results', [])
            if results and results[0].get('media'):
                media = results[0]['media']
                images = [m for m in media if m.get('type') == 'StillImage']
                if images:
                    print(f"GBIF Found image for {species_name}: {images[0].get('identifier')}")
                    return True
    except Exception as e:
        print(f"GBIF Error for {species_name}: {e}")
    print(f"GBIF No image found for {species_name}")
    return False

def test_wiki(species_name):
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&titles={urllib.parse.quote(species_name)}&pithumbsize=800&format=json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'CollembolaScraper/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())
            pages = data.get('query', {}).get('pages', {})
            for page_id, page_info in pages.items():
                if page_id != '-1' and 'thumbnail' in page_info:
                    print(f"Wiki Found image for {species_name}: {page_info['thumbnail']['source']}")
                    return True
    except Exception as e:
        print(f"Wiki Error for {species_name}: {e}")
    print(f"Wiki No image found for {species_name}")
    return False

species = ["Onychiurus cunhai", "Folsomia candida", "Isotomurus maculatus"]
for s in species:
    test_gbif_occurrence(s)
    test_wiki(s)
