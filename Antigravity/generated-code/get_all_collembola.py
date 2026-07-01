import urllib.request
import urllib.parse
import json
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def query_api(endpoint):
    url = f"https://fauna.jbrj.gov.br/rest/{endpoint}"
    req = urllib.request.Request(url, headers=headers)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            print(f"Error querying {url}: {e}. Retrying in 1s...")
            time.sleep(1)
    return []

# Collembola class ID is 245312
class_id = 245312

all_taxa = {}
queue = [class_id]
ranks_count = {}

# We will fetch level by level
while queue:
    print(f"Queue size: {len(queue)}")
    # We can batch query in groups of 50 to avoid too long URLs
    batch_size = 50
    for i in range(0, len(queue), batch_size):
        batch = queue[i:i+batch_size]
        if len(batch) == 1:
            query = f"v_taxon_data?idtaxon_pai=eq.{batch[0]}"
        else:
            ids_str = ",".join(map(str, batch))
            query = f"v_taxon_data?idtaxon_pai=in.({ids_str})"
        
        children = query_api(query)
        next_queue = []
        for child in children:
            tid = child['id_taxon']
            if tid not in all_taxa:
                all_taxa[tid] = child
                ranks_count[child['rank']] = ranks_count.get(child['rank'], 0) + 1
                # If rank is not ESPECIE or SUB_ESPECIE, we can traverse deeper
                if child['rank'] not in ('ESPECIE', 'SUB_ESPECIE'):
                    next_queue.append(tid)
        
    queue = next_queue

print("\nTraversed taxons by rank:")
for rank, count in ranks_count.items():
    print(f"  {rank}: {count}")

print(f"Total taxa found: {len(all_taxa)}")

# Let's save all_taxa to a file to examine the data
with open("C:/Users/Guilherme/.gemini/antigravity/brain/dfe1eb06-5940-4b05-80d0-b157521e1600/scratch/collembola_taxa.json", "w", encoding="utf-8") as f:
    json.dump(all_taxa, f, ensure_ascii=False, indent=2)
print("Saved to collembola_taxa.json")
