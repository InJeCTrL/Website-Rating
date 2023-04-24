import boto3
import os

client = boto3.client('dynamodb')

def handler(event, context):
    return "Empty now"
'''
    client.update_item(
        TableName=os.getenv('RATINGTABLE'),
        Key={'string': 'host'},
        UpdateExpression='SET good = good + :incr',
        ExpressionAttributeValues={':incr': 1},
        ReturnValues="ALL_NEW"
    )
'''