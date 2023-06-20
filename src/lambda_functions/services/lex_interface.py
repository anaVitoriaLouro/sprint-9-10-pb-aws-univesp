import os
import json
import boto3
from dotenv import load_dotenv
from services.textRekognition import img2txt

load_dotenv()

# Retrieve environment variables
LEX_BOT_ID = os.environ['LEX_BOT_ID']
LEX_BOT_ALIAS_ID = os.environ['LEX_BOT_ALIAS_ID']
LEX_BOT_REGION = os.environ['LEX_BOT_REGION']

# Create a client for Lex runtime
lex_client = boto3.client('lexv2-runtime', region_name=LEX_BOT_REGION)

def handle_lex_event(event, context):
  # Retrieve session state and intent information from the event
  print('handle_lex_event foi invocada')
  print(event)
  session_state = event['sessionState']
  intent_name = session_state['intent']['name']
  state = session_state['intent']['state']
  image_path = session_state['intent']['slots']['ImagePath'] #s3-url da imagem contendo texto
  # image_url = session_state['intent']['slots']['ImageURL'] # url da imagem passada pro slot, que na vdd é a o nome da imagem como está armazenada no bucket

  # Remove the 'ImagePath' slot if it is None
  if image_path is None:
    session_state['intent']['slots'].pop('ImagePath', None)

  # Determine the dialog action type and slot to elicit for the response
  if 'proposedNextState' in event:
    dialog_action = event['proposedNextState']['dialogAction']
    dialog_action_type = dialog_action['type']
    slot_to_elicit = dialog_action['slotToElicit']
  else:
    dialog_action_type = 'Delegate'
    slot_to_elicit = None

  # Prepare the dialog action response
  dialog_action_response = {
    "type": dialog_action_type
  }

  # Include the slot to elicit if applicable
  if slot_to_elicit:
    slot_to_elicit = dialog_action_response['slotToElicit']

  # Include the intent name and state if applicable
  if intent_name:
    dialog_action_response['intent'] = {'name': intent_name}
  if dialog_action_type == 'Delegate':
    state = dialog_action_response['state']

  # Update the session state with the dialog action response
  dialog_action_response = session_state['dialogAction']

  # Create the final response object
  response = {
    "sessionState": session_state,
  }

  # Process the target age and image_path if both are available
  if image_path is not None and 'value' in image_path:
    image_to_process = image_path['value']['interpretedValue']

    print(f'so pra ver se pegou o image_path: {image_path}')

    print('depois desse print deveria chamar o rekognition')

    # AQUI PODE CHAMAR O REKOGNITION PASSANDO APENAS A image_to_transcribe QUE É A KEY DO OBJETO ARMAZENADO NO BUCKET
    processed_image = img2txt(image_to_process)
    print(f'This is the processed image. It should be an URL with an audio file in S3: {processed_image}')

    print('aqui já era pra ter chamado o reko chamar o rekognition')
    
    # Update the session attributes and confirmation state
    response['sessionState']['sessionAttributes']['ImagePath'] = processed_image
    response['sessionState']['intent']['confirmationState'] = 'Confirmed'
    

    print(f'This is the response from lex_interface(handle_lex_event): {response}')
    return response

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