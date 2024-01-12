import requests
from pathlib import Path


def cpationgen(image):
    # api_url = "https://api-production-43c4.up.railway.app/predict-caption"
    api_url = "http://127.0.0.5:8000/predict-caption"

    # Make the API request
    response = requests.post(api_url, files=image)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        predicted_caption = data.get("predicted_caption")

        return predicted_caption
    else:
        return response.text
