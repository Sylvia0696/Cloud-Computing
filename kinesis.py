import json
import base64
import boto3
def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('number')
    for record in event['Records']:
        #Kinesis data is base64 encoded so decode here
        payload = base64.b64decode(record["kinesis"]["data"])
        print(payload)
        payload = payload.decode('utf-8')
        print(payload)
        print(type(payload))
        payload = json.loads(payload)
        print(payload)

        try:
            restaurant_id = payload['id']
            delta_num = payload['number']
        
            entry = table.get_item(
                Key = {'id': restaurant_id}
            )
        
            print(entry)
            item = entry['Item']
            cur_cnt = int(item['count'])
            new_cnt = cur_cnt + int(delta_num)
            
            table.update_item(
                Key={
                    'id': restaurant_id
                },
                UpdateExpression='SET #cnt = :val1',
                ExpressionAttributeValues={
                    ':val1':new_cnt
                },
                ExpressionAttributeNames={
                    '#cnt': 'count'
                }
            )
            
            entry = table.get_item(
                Key = {'id': restaurant_id}
            )
            print("second" + str(entry))
            
            
            """ this is the code for searching restaurant from dynamodb by name
            response = table.scan(
                FilterExpression=Attr('restaurant_name').eq(blabla)
            )
            items = response['Items']
            print(items)
            """
            
        except Exception as e:
            print('Error: {}'.format(e))
            print('Current data: {}'.format(payload))
    
    
    return {
        'statusCode':200,
        'body':json.dumps('Hello from Lambda!')
    }