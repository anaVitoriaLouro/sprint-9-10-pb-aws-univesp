from twilio.rest import Client

def lambda_handler(event, context):
    # Parâmetros da mensagem a ser enviada
    from_number = "+1234567890"  # Número Twilio
    to_number = event['queryStringParameters']['to']  # Número de destino
    message_body = "Olá! Esta é uma mensagem enviada pelo Twilio."

    # Credenciais do Twilio
    account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
    auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
    
    # Criando uma instância do cliente Twilio
    client = Client(account_sid, auth_token)

    # Enviando a mensagem usando o cliente Twilio
    message = client.messages.create(
        body=message_body,
        from_=from_number,
        to=to_number
    )

    # Retornando uma resposta
    response = {
        "statusCode": 200,
        "body": f"Mensagem enviada com sucesso! SID: {message.sid}"
    }

    return response
