import base64
import os
import boto3
import json
from botocore.exceptions import ClientError

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
    
    remote_ip = event['requestContext']['http']['sourceIp']
    
    data = json.loads(str(base64.b64decode(event['body']), "utf-8"))
    handler_response['body']['host'] = data['host']
    operation = data['operation']
    
    update_expression = (\
        ('SET good = if_not_exists(good, :zero) + :incr, ' + \
        'bad = if_not_exists(bad, :zero) ') if operation == '+' else \
        ('SET good = if_not_exists(good, :zero), ' + \
        'bad = if_not_exists(bad, :zero) + :incr ')
    ) + 'ADD submitted :remote_ip_list'
    
    try:
        response = client.update_item(
            TableName=os.getenv('RATINGTABLE'),
            Key={'host': {
                'S': data['host']
            }},
            UpdateExpression=update_expression,
            ExpressionAttributeValues={
                ':incr': {
                    'N': '1'
                },
                ':zero': {
                    'N': '0'
                },
                ':remote_ip_list': {
                    'SS': [
                        remote_ip
                    ]
                },
                ':remote_ip': {
                    'S': remote_ip
                }},
            ReturnValues="ALL_NEW",
            ConditionExpression="NOT contains(submitted, :remote_ip)"
        )

        handler_response['body']['good'] = int(response['Attributes']['good']['N'])
        handler_response['body']['bad'] = int(response['Attributes']['bad']['N'])
    except ClientError as err:
        if err.response['Error']['Code'] == "ConditionalCheckFailedException":
            handler_response['body']['msg'] = "Don't submit repeatedly!"
            handler_response['statusCode'] = 400
        
    return handler_response