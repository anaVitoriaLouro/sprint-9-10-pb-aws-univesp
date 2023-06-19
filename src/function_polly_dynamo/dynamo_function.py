import boto3
import json
import os
from random import randint

# nome da tabela do dynamo
tableName = "phrases-table-dev"

# criando recurso dynamodb
dynamo = boto3.resource('dynamodb').Table(tableName)

print('Carregando')

def ddb_raffle():
        n = randint(1,3)
        element = dynamo.get_item(
            Key = {
                    "id": n
                })
        return element['Item']['phrase']

def get_phrase(event, context):
    print(event)
    body = json.loads(event['body'])
    
    # CRUD
    def ddb_create(x):
        dynamo.put_item(**x)

    def ddb_read(x):
        return dynamo.get_item(**x)

    def ddb_update(x):
        dynamo.update_item(**x)
        
    def ddb_delete(x):
        dynamo.delete_item(**x)

    def echo(x):
        return x

    def ddb_list(x):
        response = dynamo.scan()
        return response['Items']

    operation = body['operation']

    operations = {
        'create': ddb_create,
        'read': ddb_read,
        'update': ddb_update,
        'delete': ddb_delete,
        'echo': echo,
        'list': ddb_list,
    }

    if operation in operations:
        return operations[operation](body['payload'])
    elif operation == 'raffle':
        return ddb_raffle()
    else:
        raise ValueError('Operação desconhecida "{}"'.format(operation))