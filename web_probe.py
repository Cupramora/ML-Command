# web_probe.py

import requests, os, time, json
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from perception import process_capsule, PerceptionCapsule

HEADERS = {"User-Agent": "Mozilla/5.0"}
ARCHIVE_DIR = "encyclopedia"
LOG_FILE = "web_probe_log.jsonl"

os.makedirs(ARCHIVE_DIR, exist_ok=True)

def probe_and_perceive(concept: str, max_images: int = 5):
    query = concept.replace(" ", "+")
    url = f"https://www.google.com/search?tbm=isch&q={query}"
    r = requests.get(url, headers=HEADERS, timeout=5)
    soup = BeautifulSoup(r.text, "html.parser")

    image_urls = []
    for img in soup.find_all("img"):
        src = img.get("src")
        if src and src.startswith("http"):
            image_urls.append(src)
        if len(image_urls) >= max_images:
            break

    results = []

    for i, img_url in enumerate(image_urls):
        try:
            img_data = requests.get(img_url, headers=HEADERS, timeout=5).content
            img = Image.open(BytesIO(img_data)).convert("RGB")

            # Save image to concept folder
            concept_dir = os.path.join(ARCHIVE_DIR, concept)
            os.makedirs(concept_dir, exist_ok=True)
            img_path = os.path.join(concept_dir, f"{concept}_{i}.jpg")
            img.save(img_path)

            # Build and process capsule
            capsule = PerceptionCapsule(
                stimulus={"source": "web_probe", "image_path": img_path},
                emotion_vector={"curiosity": 0.6},
                behavior="web_learning",
                context=f"Web image of {concept}",
                feedback="neutral",
                reinforcement=0.2
            )

            result = process_capsule(capsule)
            result["image_path"] = img_path
            results.append(result)

            # Log result
            with open(LOG_FILE, "a") as f:
                f.write(json.dumps(result, indent=2) + "\n")

        except Exception as e:
            print(f"[WebProbe] Error processing image {i}: {e}")

    return results