import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
def lambda_handler(event, context):
    print("event",event)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('business')
    
    response = table.scan(FilterExpression=Attr('location').contains(event['labels'][0]['q']))
    items = response['Items']
    count = 4
    res=[]
    for i in items:
        if count == 0:
            break
        res.append(i)
        count -= 1
        
    return {
        "greeting": res
    }

def lambda_handler(event, context):
    print("event",event)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('business')
    
    response = table.scan(FilterExpression=Attr('category').contains(event['labels'][0]['q']))
    items = response['Items']
    count = 4
    res=[]
    for i in items:
        if count == 0:
            break
        res.append(i)
        count -= 1
        
    return {
        "greeting": res
    }

def lambda_handler(event, context):
    print("event",event)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('business')
    
    response = table.scan(FilterExpression=Attr('name').contains(event['labels'][0]['q']))
    items = response['Items']
    count = 4
    res=[]
    for i in items:
        if count == 0:
            break
        res.append(i)
        count -= 1
        
    return {
        "greeting": res
    }

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('number')
    text = event["message"]["word"]
    texts = text.split(',')
    res=[]
    for i in texts:
        entry = table.get_item(Key = {'id': i})
        item = entry['Item']
        res.append(item)
    
    return{
        "greeting":res
    }
    
def lambda_handler(event, context):
    print("event",event)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('business')
    
    response = table.scan(FilterExpression=Attr('feature').contains(event['labels'][0]['q']))
    items = response['Items']
    count = 4
    res=[]
    for i in items:
        if count == 0:
            break
        res.append(i)
        count -= 1
        
    return {
        "greeting": res
    }

def lambda_handler(event, context):
    print("event",event)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('business')
    price=""
    if int(event['labels'][0]['q']) > 60:
        price="$$$$"
    elif int(event['labels'][0]['q']) > 30:
        price="$$$"
    elif int(event['labels'][0]['q']) > 15:
        price="$$"
    else:
        price="$"
        
    # price = unicode(price, 'utf-8')
    response = table.scan(FilterExpression=Attr('price').eq(price))
    items = response['Items']
    count = 4
    res=[]
    for i in items:
        if count == 0:
            break
        res.append(i)
        count -= 1
        
    return {
        "greeting": res
    }