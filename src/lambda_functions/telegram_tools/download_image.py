import os
import json
import boto3
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']

def download_image(file_id, file_unique_id):
    # Create an S3 client
    s3 = boto3.client('s3')

    # Get the file path from the response of the uploaded image from Telegram
    response = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getFile?file_id={file_id}")
    photo_path = response.json()['result']['file_path']

    # Download the actual image content from Telegram
    photo_content = requests.get(f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{photo_path}").content

    # Extract the image format from the file path
    image_format = photo_path.split(".")[-1]

    # Generate a unique file key to store the image in S3
    file_key = f"photos/{file_unique_id}.{image_format}"

    # Upload the image content to S3
    s3.put_object(Bucket=os.environ['IMAGE_INPUT_BUCKET_NAME'], Key=file_key, Body=photo_content)

    # Generate a presigned URL for accessing the uploaded image from S3
    url = s3.generate_presigned_url('get_object', Params={'Bucket': os.environ['IMAGE_INPUT_BUCKET_NAME'], 'Key': file_key}, ExpiresIn=3600)

    # Print the URL generated from S3 for debugging purposes
    print(url)

    # Return the file key of the uploaded image
    return file_key