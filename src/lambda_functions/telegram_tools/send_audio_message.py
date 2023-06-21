import requests
import json

def telegram_send_audio(audio_url, chat_id, telegram_token):
  try:
    # Download the audio file sent by the user from the audio URL
    response = requests.get(audio_url)
    audio_data = response.content

    # Prepare the URL for sending the audio using the Telegram Bot API
    url = f"https://api.telegram.org/bot{telegram_token}/sendAudio"

    # Prepare the data and files for the POST request
    data = {"chat_id": chat_id}
    files = {"audio": ("audio_file.mp3", audio_data)}

    # Send the audio to the Telegram chat (is this the lex bot's response?)
    response = requests.post(url, data=data, files=files)

    # Check if the request was successful
    if response.status_code != 200:
      # Raise an exception with an error message if the request failed
      raise Exception(f"Error sending the audio to chat {chat_id}: {response.text}")

    # Return the response text
    return response.text

  except Exception as e:
    # Print the exception and return an error response
    print(e)
    return {
      'statusCode': 500,
      'body': json.dumps(str(e))
    }