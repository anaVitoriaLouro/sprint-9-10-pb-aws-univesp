import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import io
import sys
import uuid

polly = boto3.client("polly")
s3 = boto3.client("s3")

def synthetize_speech(text, bucket_name):
  
  object_prefix = str(uuid.uuid4().hex)

  try:
    # Request speech synthesis
    response = polly.synthesize_speech(
        Engine="neural",
        LanguageCode="pt-BR",
        TextType="text",
        Text=text,
        OutputFormat="mp3",
        VoiceId="Camila",
    )

  except (BotoCoreError, ClientError) as error:
    print(f"The service returned an error, exit gracefully: {error}")
    sys.exit(-1)

  # Access the audio stream from the response
  if "AudioStream" in response:
    # Note: Closing the stream is important because the service throttles on the
    # number of parallel connections. Here we are using contextlib.closing to
    # ensure the close method of the stream object will be called automatically
    # at the end of the 'with' statement's scope.
    with closing(response["AudioStream"]) as stream:
      # Create a BytesIO object to store the audio in memory
      audio_data = io.BytesIO()
      audio_data.write(stream.read())
      audio_data.seek(0)

      # Upload the synthesized audio file to S3
      s3_bucket = bucket_name
      s3_key = str(object_prefix) + "_synthesized_audio.mp3"

    try:
      s3.upload_fileobj(audio_data, s3_bucket, s3_key)
      print("Synthesized audio uploaded to S3 successfully.")
    except (BotoCoreError, ClientError) as error:
      print(f"Error uploading the synthesized audio to S3: {error}")
      sys.exit(-1)

  else:
    # The response didn't contain audio data, exit gracefully
    print("Could not stream audio")
    sys.exit(-1)
