import os
import json
import boto3
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']

def telegram_send_image(image_url, chat_id):
  try:
    # Download the image sent by the user from the Telegram URL
    response = requests.get(image_url)

    # Prepares the URL for sending the photo using the Telegram Bot API
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"

    # Prepare the data and files for the POST request
    data = {"chat_id": chat_id}
    files = {"photo": response.content}

    # Send the image to the Telegram chat (is this the lex bot's response?)
    response = requests.post(url, data=data, files=files)

    # Check if the request was successful
    if response.status_code != 200:
      # Raise an exception with an error message if the request failed
      raise Exception(f"Error sending the image to chat {chat_id}: {response.text}")

    # Return the response text
    return response.text

  except Exception as e:
    # Print the exception and return an error response
    print(e)
    return {
      'statusCode': 500,
      'body': json.dumps(str(e))
    }