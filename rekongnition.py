import json
import boto3
import base64
from boto3.dynamodb.conditions import Key, Attr
def lambda_handler(event, context):

    print(event)
    print(context)
    print(event['data'])
    print(type(event['data']))
    print(len(event['data']))
    img = base64.b64decode(event['data'])
    
    rekognition = boto3.client('rekognition')
    response = rekognition.detect_labels(Image={'Bytes':img}, MaxLabels=10, MinConfidence=70)
    print(response)
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('food')
    
    response = table.scan(FilterExpression=Attr('name').contains(response['Labels'][0]['Name']))
    items = response['Items']
    count = 4
    res=[]
    for i in items:
        if count == 0:
            break
        res.append(i)
        count -= 1
    
    return {
        'greeting': res
    }
