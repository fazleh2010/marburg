import json

# Path to your JSON file
dir = "/documents/"
json_path = dir + "extracted_images/book_Bruggen_Israels_Machtelt_Piero_del.json"

# Load JSON
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Collect all paragraphs
all_paragraphs = []
for page in data:
    page_num = page.get("page")
    for para in page.get("paragraphs", []):
        all_paragraphs.append({
            "page": page_num,
            "paragraph": para.strip()
        })

# Print all paragraphs
for p in all_paragraphs:
    print(f"Page {p['page']}: {p['paragraph']}\n")
    break


print(f"\n✅ Loaded {len(all_paragraphs)} paragraphs from {json_path}")
