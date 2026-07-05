import urllib.request
import urllib.parse
import json

def test_inaturalist(species_name):
    print(f"Testing iNaturalist for {species_name}")
    try:
        url = f"https://api.inaturalist.org/v1/taxa?q={urllib.parse.quote(species_name)}&per_page=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'CollembolaScraper/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())
            results = data.get('results', [])
            if results and results[0].get('default_photo'):
                photo = results[0]['default_photo']
                print(f"Found image: {photo.get('medium_url')}")
            else:
                print("No image found.")
    except Exception as e:
        print(f"Error: {e}")

def test_gbif(species_name):
    print(f"Testing GBIF for {species_name}")
    try:
        # First get taxon key
        url = f"https://api.gbif.org/v1/species/match?name={urllib.parse.quote(species_name)}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())
            key = data.get('usageKey')
            if not key:
                print("Taxon not found.")
                return
        
        # Then get media
        url = f"https://api.gbif.org/v1/species/{key}/media"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())
            results = data.get('results', [])
            images = [m for m in results if m.get('type') == 'StillImage']
            if images:
                print(f"Found image: {images[0].get('identifier')}")
            else:
                print("No image found.")
    except Exception as e:
        print(f"Error: {e}")

species = ["Onychiurus cunhai", "Sminthurides aquaticus", "Sphaeridia fibulifera", "Folsomia candida"]
for s in species:
    test_inaturalist(s)
    test_gbif(s)
    print("-" * 30)
