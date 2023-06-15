from services.lex_interface import lex_view_message
from telegram_tools.send_audio_message import send_audio
from telegram_tools.send_image_message import send_image
from telegram_tools.send_text_message import send_text

def manage_messages(message, session_id, chat_id):
  try:
    # Send message to Lex and wait to get the response
    lex_response = lex_view_message(message, session_id)
    # Print Lex response for debug
    print(f'THIS IS THE LEX RESPONSE: {lex_response}')

    # Extract intent and session attributes from Lex response
    intent = lex_response['sessionState']['intent']
    session_attributes = lex_response['sessionState']['sessionAttributes']


    # /     \     /     \     /     \     /     \     /     \     /     \     

    # IMPLEMENTAR A PARTIR DAQUI

    # Check if the intent confirmation state is 'Confirmed' to send the image
    if 'confirmationState' in intent and intent['confirmationState'] == 'Confirmed':

      
      # *** Aqui precisa checar se a URL da imagem veio na resposta do Lex ***
      if 'AgeProgressionImage' in session_attributes:
        # Get the image URL from session attributes
        image_url = session_attributes['AgeProgressionImage']

        # Send the image to Telegram
        response = send_image(image_url, chat_id)
        # This is the response directly from lex
        print(f'PRINT RESPONSE FOR DEBUG: {response.text}')

    # /     \     /     \     /     \     /     \     /     \     /     \     

    # IMPLEMENTAR A PARTIR DAQUI

    # NESSA PARTE PRECISA FAZER UM IF PRA VER SE TEM A URL DO AUDIO NA RESPOSTA DO LEX, SE TIVER, ENVIAR PRO TELEGRAM
    # ACHO QUE DA PRA SEGUIR A MESMA LÓGICA DO QUE TÁ ACIMA NO CASO DE UMA IMAGEM
    # if 'confirmationState' in intent and intent['confirmationState'] == 'Confirmed':
    #   if 'audio' in session_attributes:
    #     audiofile_url = ???
    # # Send the image to Telegram
    #     response = send_image(image_url, chat_id)
    #     # This is the response directly from lex
    #     print(f'PRINT RESPONSE FOR DEBUG: {response.text}')

    # /     \     /     \     /     \     /     \     /     \     /     \   

    # Check if there are any PlainText messages in the Lex response
    if 'messages' in lex_response:
      messages = [message['content'] for message in lex_response['messages'] if message['contentType'] == 'PlainText']
      if messages:
        # Send the messages to Telegram
        response = send_text(messages, chat_id)
        print(f'PRINT PLAIN_TEXT LEX RESPONSE FOR DEBUG {response.text}')

        # Return the response as the API response
        return {
          'statusCode': response.status_code,
          'body': response.text
        }
  
  except Exception as e:
    return {
			'statusCode': 500,
			'body': f'Something bad has happened, run to the hills! This is why: {str(e)}'
		}
