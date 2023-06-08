import json
import boto3

def health(event, context):
  body = {
      "message": "health funciona até aqui",
      "input": event,
  }

  response = {"statusCode": 200, "body": json.dumps(body)}

  return response

def transcribeAudio(event, context):
  try:
    body = json.loads(event['body'])
    key = body['key']
    value = body['value']
    
    response = (key, value)
    print(response)

    return {
      'statusCode': 200,
      'body': json.dumps(response)
    }
    
  except json.JSONDecodeError:
    return {
      'statusCode': 500,
      'body': json.dumps({'error': 'Invalid JSON payload'})
    }

def transcribeText(event, context):
  try:
    body = json.loads(event['body'])
    key = body['key']
    value = body['value']
    
    response = (key, value)
    print(response)

    return {
      'statusCode': 200,
      'body': json.dumps(response)
    }
    
  except json.JSONDecodeError:
    return {
      'statusCode': 500,
      'body': json.dumps({'error': 'Invalid JSON payload'})
    }

def rekognition(event, context):
  try:
    body = json.loads(event['body'])
    key = body['key']
    value = body['value']
    
    response = (key, value)
    print(response)

    return {
      'statusCode': 200,
      'body': json.dumps(response)
    }
    
  except json.JSONDecodeError:
    return {
      'statusCode': 500,
      'body': json.dumps({'error': 'Invalid JSON payload'})
    }
  