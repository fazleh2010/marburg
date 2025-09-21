import pdfplumber
import clip
import torch
from PIL import Image
import torch.nn.functional as F

# --- Settings ---
pdf_path = "/home/melahi/code/marburg/documents/corpus_texts/book_Bruggen_Israels_Machtelt_Piero_del.pdf"  # Path to your PDF
image_path = "/home/melahi/code/marburg/documents/extracted_images/page1_img1.jpeg"      # Path to the image
device = "cuda" if torch.cuda.is_available() else "cpu"

# --- Load CLIP model ---
model, preprocess_clip = clip.load("ViT-B/32", device=device)

# --- Extract text from PDF ---
def extract_text_from_pdf(pdf_path):
    all_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            all_text += page.extract_text() + "\n\n"
    return all_text

document_text = extract_text_from_pdf(pdf_path)

# --- Split document into paragraphs (or windows of sentences) ---
paragraphs = [p.strip() for p in document_text.split("\n\n") if p.strip()]

# --- Encode the image ---
image = preprocess_clip(Image.open(image_path)).unsqueeze(0).to(device)
with torch.no_grad():
    image_features = model.encode_image(image)

# --- Encode all text paragraphs ---
text_features_list = []
for para in paragraphs:
    text_tokens = clip.tokenize([para]).to(device)
    with torch.no_grad():
        text_features = model.encode_text(text_tokens)
    text_features_list.append(text_features)

# --- Compute similarity ---
similarities = [F.cosine_similarity(image_features, tf).item() for tf in text_features_list]

# --- Find most relevant paragraph ---
best_idx = similarities.index(max(similarities))
print("Most relevant paragraph for the image:\n")
print(paragraphs[best_idx])
