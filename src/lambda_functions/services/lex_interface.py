import os
import json
import boto3
from dotenv import load_dotenv
from services.text_rekognition import img2txt

load_dotenv()

# Retrieve environment variables
LEX_BOT_ID = os.environ['LEX_BOT_ID']
LEX_BOT_ALIAS_ID = os.environ['LEX_BOT_ALIAS_ID']
LEX_BOT_REGION = os.environ['LEX_BOT_REGION']

# Create a client for Lex runtime
lex_client = boto3.client('lexv2-runtime', region_name=LEX_BOT_REGION)

def lex_view_message(message, session_id):
  # Print the message and its type for debugging
  # print(f'message: {message}; message type: {type(message)}')

  try:
    # Send the message to Lex for recognition
    response = lex_client.recognize_text(
      botId=LEX_BOT_ID,
      botAliasId=LEX_BOT_ALIAS_ID,
      localeId='pt_BR',
      sessionId=session_id,
      text=message,
    )

    # Print the Lex response for debugging
    # print(f'This is the LEX RESPONSE from lex_interface(lex_view_message){response}')
    print(f'lex respondeu')
    
    return response
  
  except Exception as e:
    # Print the exception and return an error response
    print(f'An error caused a system crash, please check: {e}')

    return {
      'statusCode': 500,
      'body': json.dumps(str(e))
    }