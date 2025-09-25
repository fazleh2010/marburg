import json
import os

def extract_best_paragraphs(input_json: str, output_json: str) -> None:
    """
    Extracts the best paragraph (highest similarity) per image from a JSON file
    and saves the results to a new JSON file.

    Args:
        input_json (str): Path to input JSON file.
        output_json (str): Path to save the filtered JSON file.
    """
    # Load data
    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Dictionary to store the best paragraph per image
    best_paragraphs = {}

    for entry in data:
        paragraph_text = entry["original_text"]
        page = entry["page"]
        para_num = entry["paragraph_number"]

        # Each entry has a "results" list with multiple images and similarity scores
        for res in entry["results"]:
            image = res["image"]
            similarity = res["similarity"]

            # Keep the paragraph with the highest similarity for each image
            if image not in best_paragraphs or similarity > best_paragraphs[image]["similarity"]:
                best_paragraphs[image] = {
                    "page": page,
                    "paragraph_number": para_num,
                    "paragraph": paragraph_text,
                    "similarity": similarity
                }

    # Convert dictionary to a list for JSON output
    output_data = [
        {
            "image": image,
            "page": info["page"],
            "paragraph_number": info["paragraph_number"],
            "paragraph": info["paragraph"],
            "similarity": info["similarity"]
        }
        for image, info in best_paragraphs.items()
    ]

    # Write to JSON file
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Best paragraphs per image saved to: {output_json}")


# Run for all *_results.json files in output_dir
if __name__ == "__main__":
    output_dir = "/home/melahi/code/documents/output/"

    for filename in os.listdir(output_dir):
        if filename.endswith("_results.json") and not filename.endswith("_best.json"):
            input_json = os.path.join(output_dir, filename)

            # Insert "_best" before the .json extension
            base, ext = os.path.splitext(filename)
            output_json = os.path.join(output_dir, f"{base}_best{ext}")

            extract_best_paragraphs(input_json, output_json)
