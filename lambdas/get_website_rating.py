import base64
import os
import boto3
import json

client = boto3.client('dynamodb')

def handler(event, context):
    handler_response = {
        'statusCode': 200,
        'body': {
            'host': '',
            'good': 0,
            'bad': 0
        },
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
    }
    
    if 'body' not in event:
        handler_response['statusCode'] = 400
        handler_response['body']['msg'] = "Empty host!"
        return handler_response
    
    host = json.loads(str(base64.b64decode(event['body']), "utf-8"))['host']
    handler_response['body']['host'] = host
    
    response = client.get_item(
        TableName=os.getenv('RATINGTABLE'),
        Key={'host': {
            'S': host
        }}
    )
    
    if 'Item' not in response:
        return handler_response
    
    handler_response['body']['good'] = int(response['Item']['good']['N'])
    handler_response['body']['bad'] = int(response['Item']['bad']['N'])

    return handler_response