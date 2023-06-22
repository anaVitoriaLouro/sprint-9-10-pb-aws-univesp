import os
import json
import boto3

# Recupera as variáveis de ambiente
LEX_BOT_ID = os.environ['LEX_BOT_ID']
LEX_BOT_ALIAS_ID = os.environ['LEX_BOT_ALIAS_ID']
LEX_BOT_REGION = os.environ['LEX_BOT_REGION']

# Cria um cliente para o Lex runtime
lex_client = boto3.client('lexv2-runtime', region_name=LEX_BOT_REGION)

def lex_messages(message, session_id):
    try:
        # Envia a mensagem para o Lex para reconhecimento
        response = lex_client.recognize_text(
            botId=LEX_BOT_ID,
            botAliasId=LEX_BOT_ALIAS_ID,
            localeId='pt_BR',
            sessionId=session_id,
            text=message,
        )

        print(f'Sucesso!')
        return response

    except Exception as e:
        # Em caso de erro, imprime a exceção e retorna uma resposta de erro
        print(f'Pane no sistema!{e}')

        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }