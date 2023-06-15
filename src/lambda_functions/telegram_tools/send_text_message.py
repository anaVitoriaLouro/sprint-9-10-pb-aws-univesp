import os
import json
import boto3
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']

def telegram_send_messages(messages, chat_id):
  try:
    # Prepares the URL for sending the photo using the Telegram Bot API
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    # Set the headers for the request
    headers = {
      'Content-Type': 'application/json'
    }
    
    # Iterate over each message in the list
    for message in messages:
      # Prepare the data for the request
      data = {
        'text': message,
        'chat_id': chat_id
      }

      # Send the message to Telegram using a POST request
      response = requests.post(url, headers=headers, json=data)
      
      # Check in case the request wasn't successful
      if response.status_code != 200:
        # Raise an exception message if the request failed
        raise Exception(f"Error sending message: {response.text} to {chat_id}. Error: {response.status_code}")
     
    return response
  
  except Exception as e:
    return {
			'statusCode': 500,
			'body': f'Sorry! Could not send the message to Telegram: {str(e)}'
		}
 