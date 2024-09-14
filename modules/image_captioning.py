import requests

API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query_image_captioning(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()
