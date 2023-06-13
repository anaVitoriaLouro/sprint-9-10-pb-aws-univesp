import os
from services.synthetize_speech import synthetize_speech

BUCKET_NAME = os.environ['BUCKET_NAME']

def get_speech(body):
  try:
    if "text" in body["event"] and body["event"]["text"]:
      text = body["event"]["text"]
        
      print('synthetize_speech STARTED')
      synthetize_speech(text, BUCKET_NAME)
      print('synthetize_speech COMPLETED')
      
      return {
        'statusCode': 200,
        'body': 'Speech was uploaded to your S3Bucket.'
      }
    
  except Exception as e:
    print(f'Get speech job failed with delight. Reason: {e}')