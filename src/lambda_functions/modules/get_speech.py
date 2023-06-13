import os
from services.synthesize_speech import synthesize_speech

BUCKET_NAME = os.environ['SYNTHESIZED_SPEECH_BUCKET_NAME']

def get_speech(body):
  try:
    if "text" in body["event"] and body["event"]["text"]:
      text = body["event"]["text"]
        
      print('synthesize_speech STARTED')
      synthesize_speech(text, BUCKET_NAME)
      print('synthesize_speech COMPLETED')
      
      return {
        'statusCode': 200,
        'body': 'Speech was uploaded to your S3Bucket.'
      }
    
  except Exception as e:
    print(f'Get speech job failed with delight. Reason: {e}')