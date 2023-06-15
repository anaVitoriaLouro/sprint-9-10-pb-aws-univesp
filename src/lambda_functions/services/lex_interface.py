import os
import json
import boto3
from services.textRekognition import img2txt
from dotenv import load_dotenv

load_dotenv()

# Retrieve environment variables
LEX_BOT_ID = os.environ['LEX_BOT_ID']
LEX_BOT_ALIAS_ID = os.environ['LEX_BOT_ALIAS_ID']
LEX_BOT_REGION = os.environ['LEX_BOT_REGION']

# Create a client for Lex runtime
lex_client = boto3.client('lexv2-runtime', region_name=LEX_BOT_REGION)

def handle_lex_event(event, context):
  # Retrieve session state and intent information from the event
  session_state = event['sessionState']
  intent_name = session_state['intent']['name']
  state = session_state['intent']['state']
  texted_img = session_state['intent']['slots']['TextedImage'] #imagem contendo texto
  image_url = session_state['intent']['slots']['ImageURL'] #url da imagem passada pro slot, que na vdd é a o nome da imagem como está armazenada no bucket

  # Remove the 'TextedImage' slot if it is None
  if texted_img is None:
    session_state['intent']['slots'].pop('TextedImage', None)

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

  # Process the target age and image URL if both are available
  if texted_img is not None and 'value' in texted_img and 'value' in image_url:
    image_to_transcribe = texted_img['value']['interpretedValue']
    image_key_value = image_url['value']['interpretedValue']

    # /     \     /     \     /     \     /     \     /     \     /     \  
    # AQUI É ONDE FAREMOS O REKOGNITION
    
    # Print result from DetectText
    #print(f' FROM lex_interface.handle_lex_event PRINT detect_text_result: {detect_text_result}')

    # Update the session attributes and confirmation state
    #processed_image = response['sessionState']['sessionAttributes']['AgeProgressionImage']
    #response['sessionState']['intent']['confirmationState'] = 'Confirmed'

    # Print the response and return it for debug
    #print(f'FROM manage_messages.handle_lex_event => PRINT RESPONSE FOR DEBUG: {response}')
    
    return response


def lex_view_message(message, session_id):
  # Print the message and its type for debugging
  print(f'message: {message}; message type: {type(message)}')

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
    print(response)
    print('recognize_text response/lex event')

    return response
  
  except Exception as e:
    # Print the exception and return an error response
    print(e)
    print('lex_send_message/lex event')

    return {
      'statusCode': 500,
      'body': json.dumps(str(e))
    }