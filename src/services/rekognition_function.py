import json
import boto3
import botocore
import datetime


def read_image(event, context):
    try:
        for record in event['Records']:
            bucket_name = record['s3']['bucket']['name']
            image_name = record['s3']['object']['key']
            criacao_imagem = dateutil.parser.parse(record['eventTime'])
    except KeyError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Missing required field: {e}'})
        }
    except json.JSONDecodeError:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Invalid JSON payload'})
        }
    
    try:
        s3_client = boto3.client('s3')
        rekognition = boto3.client("rekognition")
        response = rekognition.detectText(
            Image={'S3Object': {'Bucket': bucket_name, 'Name': image_name}}
        )

        text = response['TextDetections'][0]
      
        response = s3_client.head_object(Bucket=bucket_name, Key=image_name)
        image_url = f"https://{bucket_name}.s3.amazonaws.com/{image_name}"
        
        response_body = {
            "url_to_image": image_url,
            "created_image": creation_time,
            "text": text
        }

        response_json = json.dumps(response_body)
        
        print(response_json)

        return {
            'statusCode': 200,
            'body': response_json
        }
        
    except botocore.exceptions.ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }