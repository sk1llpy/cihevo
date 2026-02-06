import requests
from typing import List, Dict

def generate_labels_batch(labels: List[Dict], api_url: str = "https://98a2bdbb3be8.ngrok-free.app/print-labels/"):
    """
    Send multiple labels to local API for batch printing.
    Each label dict must contain: title, price_original, barcode, price_sale, logo_path, slogan
    """
    payload = {"items": labels}

    try:
        response = requests.post(api_url, json=payload, timeout=10)
        if response.ok:
            print(f"✅ Successfully printed {len(labels)} labels")
        else:
            print(f"❌ Error printing labels: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Exception occurred while printing labels: {e}")
