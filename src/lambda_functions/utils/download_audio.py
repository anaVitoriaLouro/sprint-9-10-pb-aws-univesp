import requests
import json
import os
from io import BytesIO

SLACK_TOKEN = os.environ['SLACK_TOKEN']

def download_audiofile(url, SLACK_TOKEN):
    # Set the authentication headers
    headers = {
        "Authorization": "Bearer " + SLACK_TOKEN
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    audio_content = BytesIO(response.content)

    return audio_content