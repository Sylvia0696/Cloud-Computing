
import math
import dateutil.parser
import datetime
import time
import os
import logging
import boto3
import json
from botocore.vendored import requests
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
from boto3.dynamodb.conditions import Key, Attr


""" --- Helpers to build responses which match the structure of the necessary dialog actions --- """


def get_slots(intent_request):
    return intent_request['currentIntent']['slots']


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


""" --- Helper Functions --- """


def parse_int(n):
    try:
        return int(n)
    except ValueError:
        return float('nan')


def build_validation_result(is_valid, violated_slot, message_content):
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot,
        }

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }


def isvalid_date(date):
    try:
        dateutil.parser.parse(date)
        return True
    except ValueError:
        return False


def validate_dining_config(time, date, number):
    # cuisines = ['indian', 'chinese', 'bavarian', 'british', 'french', 'japanese','korean','american']
    # if cuisine is not None and cuisine.lower() not in cuisines:
    #     return build_validation_result(False,
    #                                    'cuisine',
    #                                    'I dont\'t know about good {} restaurants, would you like a different type of food?  '
    #                                    'Our most popular restaurants are Chinese restaurant'.format(cuisine))
    # # get a dictionary of cities: 'c'
    # gc = geonamescache.GeonamesCache()
    # c = gc.get_cities()
    # 
    # # extract the US city names and coordinates
    # US_cities = [c[key]['name'] for key in list(c.keys())
    # #              if c[key]['countrycode'] == 'US']
    # city = ['new york', 'los angeles', 'chicago', 'houston', 'philadelphia', 'phoenix', 'san antonio',
    #                 'san diego', 'dallas', 'san jose', 'austin', 'jacksonville', 'san francisco', 'indianapolis',
    #                 'columbus', 'fort worth', 'charlotte', 'detroit', 'el paso', 'seattle', 'denver', 'washington dc',
    #                 'memphis', 'boston', 'nashville', 'baltimore', 'portland']
    # if location is not None and location.lower() not in city:
    #     return build_validation_result(False,
    #                                   'location',
    #                                   'Sorry, we haven\'t extended our service to {}. We are working on that!'.format(location))
    # get a dictionary of cities: 'c'
    # gc = geonamescache.GeonamesCache()
    # c = gc.get_cities()
    # 
    # # extract the US city names and coordinates
    # US_cities = [c[key]['name'] for key in list(c.keys())
    #              if c[key]['countrycode'] == 'US']
    #if phone is not None:
    #    pass
        #pho = parse_int(phone)
        #if math.isnan(pho):
            #return build_validation_result(False, 'phone', 'Sorry, this is not valid phone number. Could you check again?')

    if number is not None:
        num = parse_int(number)
        if math.isnan(num):
            return build_validation_result(False, 'NumberPeople', 'How many people are there?')

    if date is not None:
        if not isvalid_date(date):
            return build_validation_result(False, 'diningTime', 'I did not understand that, what date would you like to eat?')

    if time is not None:
        if len(time) != 5:
            # Not a valid time; use a prompt defined on the build-time model.
            return build_validation_result(False, 'diningTime', 'Not valid time format! Please try again!')

        hour, minute = time.split(':')
        hour = parse_int(hour)
        minute = parse_int(minute)
        if math.isnan(hour) or math.isnan(minute):
            # Not a valid time; use a prompt defined on the build-time model.
            return build_validation_result(False, 'diningTime', 'Not valid time format! Please try again!')

        if hour < 10 or hour > 22:
            # Outside of business hours
            return build_validation_result(False, 'diningTime', 'Restaurant hours are from 10 a m. to 10 p m. Can you specify a time during this range?')

    return build_validation_result(True, None, None)


""" --- Functions that control the bot's behavior --- """

def say_hi(intent_request):
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Hi there! How can I help you?'})

def say_bye(intent_request):
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Bye, have a good day :p'})
                  
def search_price(intent_request):
    price = get_slots(intent_request)["price"]
    location = get_slots(intent_request)["location"]
    dining_time = get_slots(intent_request)["DinningTime"]
    dining_date = get_slots(intent_request)["dinningDate"]
    number = get_slots(intent_request)["NumberPeople"]
    # phone = get_slots(intent_request)["phone"]
    source = intent_request['invocationSource']
    
    p = 0

    if price <= 15:
        p = 1
    elif price > 15 and price <= 30:
        p = 2
    elif price > 30 and price <= 45:
        p = 3
    else:
        p = 4
    
    if source == 'DialogCodeHook':
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt for the first violation detected.
        slots = get_slots(intent_request)
        print(slots)
        validation_result = validate_dining_config(dining_time, dining_date, number)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            print(slots)
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        # if cuisine is not None:
        #     output_session_attributes['Price'] = len(cuisine) * 5  # Elegant pricing model

        return delegate(output_session_attributes, get_slots(intent_request))


    headers={"Authorization": "Bearer Vv3D0MWqERhHbN7M5C1Wb1tTvsezZeISd8u6T50QI7zxkdzaLXhjQjCdRhiTqR7w1BZtPc722pRAaawBoKjgayUauLDxTV9lzfL12pwUzFVoUmAC-HUZ9s5fc_iCXHYx"}
    params={
            "term":"restaurants",
            "location":location,
            "price": p,
            "sort_by": 'rating',
            "limit": 3
        }
    myResponse = requests.get("https://api.yelp.com/v3/businesses/search", headers=headers, params=params)
    r = myResponse.json()
    r = r["businesses"]
    
    return_string = "Here are my suggestions for " + number + " people, for " +  dining_date + " " + dining_time + " :"
    return_string += " 1. " + r[0]['name'] + ", located at " + r[0]['location']['address1'] + "." 
    return_string += " 2. " + r[1]['name'] + ", located at " + r[1]['location']['address1'] + "." 
    return_string += " 3. " + r[2]['name'] + ", located at " + r[2]['location']['address1'] + "." 
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': return_string})





def search_location(intent_request):
    address = get_slots(intent_request)["address"]
    # location = get_slots(intent_request)["location"]
    dining_time = get_slots(intent_request)["DinningTime"]
    dining_date = get_slots(intent_request)["dinningDate"]
    number = get_slots(intent_request)["NumberPeople"]
    # phone = get_slots(intent_request)["phone"]
    source = intent_request['invocationSource']

    
    if source == 'DialogCodeHook':
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt for the first violation detected.
        slots = get_slots(intent_request)
        print(slots)
        validation_result = validate_dining_config(dining_time, dining_date, number)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            print(slots)
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        # if cuisine is not None:
        #     output_session_attributes['Price'] = len(cuisine) * 5  # Elegant pricing model

        return delegate(output_session_attributes, get_slots(intent_request))


    headers={"Authorization": "Bearer Vv3D0MWqERhHbN7M5C1Wb1tTvsezZeISd8u6T50QI7zxkdzaLXhjQjCdRhiTqR7w1BZtPc722pRAaawBoKjgayUauLDxTV9lzfL12pwUzFVoUmAC-HUZ9s5fc_iCXHYx"}
    params={
            "term":"restaurants",
            "location":address,
            "sort_by": 'rating',
            "limit": 3
        }
    myResponse = requests.get("https://api.yelp.com/v3/businesses/search", headers=headers, params=params)
    r = myResponse.json()
    r = r["businesses"]
    
    return_string = "Here are my suggestions for " + number + " people, for " +  dining_date + " " + dining_time + " :"
    return_string += " 1. " + r[0]['name'] + ", located at " + r[0]['location']['address1'] + "." 
    # return_string += " 2. " + r[1]['name'] + ", located at " + r[1]['location']['address1'] + "." 
    # return_string += " 3. " + r[2]['name'] + ", located at " + r[2]['location']['address1'] + "." 
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': return_string})




def search_restaurant(intent_request):
    restaurant = get_slots(intent_request)["Restaurant"]
    location = get_slots(intent_request)["location"]
    dining_time = get_slots(intent_request)["DinningTime"]
    dining_date = get_slots(intent_request)["dinningDate"]
    number = get_slots(intent_request)["NumberPeople"]
    # phone = get_slots(intent_request)["phone"]
    source = intent_request['invocationSource']

    
    if source == 'DialogCodeHook':
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt for the first violation detected.
        slots = get_slots(intent_request)
        print(slots)
        validation_result = validate_dining_config(dining_time, dining_date, number)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            print(slots)
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        # if cuisine is not None:
        #     output_session_attributes['Price'] = len(cuisine) * 5  # Elegant pricing model

        return delegate(output_session_attributes, get_slots(intent_request))


    headers={"Authorization": "Bearer Vv3D0MWqERhHbN7M5C1Wb1tTvsezZeISd8u6T50QI7zxkdzaLXhjQjCdRhiTqR7w1BZtPc722pRAaawBoKjgayUauLDxTV9lzfL12pwUzFVoUmAC-HUZ9s5fc_iCXHYx"}
    params={
            "term":restaurant,
            "location":location,
            "sort_by": 'rating',
            "limit": 3
        }
    myResponse = requests.get("https://api.yelp.com/v3/businesses/search", headers=headers, params=params)
    r = myResponse.json()
    r = r["businesses"]
    
    return_string = "Here are my suggestions for " + number + " people, for " +  dining_date + " " + dining_time + " :"
    return_string += " 1. " + r[0]['name'] + ", located at " + r[0]['location']['address1'] + "." 
    return_string += " 2. " + r[1]['name'] + ", located at " + r[1]['location']['address1'] + "." 
    return_string += " 3. " + r[2]['name'] + ", located at " + r[2]['location']['address1'] + "." 
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': return_string})






def search_feature(intent_request):
    feature = get_slots(intent_request)["feature"]
    location = get_slots(intent_request)["location"]
    dining_time = get_slots(intent_request)["DinningTime"]
    dining_date = get_slots(intent_request)["dinningDate"]
    number = get_slots(intent_request)["NumberPeople"]
    # phone = get_slots(intent_request)["phone"]
    source = intent_request['invocationSource']

    
    if source == 'DialogCodeHook':
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt for the first violation detected.
        slots = get_slots(intent_request)
        print(slots)
        validation_result = validate_dining_config(dining_time, dining_date, number)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            print(slots)
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        # if cuisine is not None:
        #     output_session_attributes['Price'] = len(cuisine) * 5  # Elegant pricing model

        return delegate(output_session_attributes, get_slots(intent_request))


    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('business')
    
    response = table.scan(FilterExpression=Attr('feature').contains(feature))
    item = response['Items']
    count = 3
    r=[]
    for i in item:
        if count == 0:
            break
        r.append(i)
        count -= 1
    
    return_string = "Here are my suggestions for " + number + " people, for " +  dining_date + " " + dining_time + " :"
    return_string += " 1. " + r[0]['name'] + ", located at " + r[0]['location'] + "." 
    return_string += " 2. " + r[1]['name'] + ", located at " + r[1]['location'] + "." 
    return_string += " 3. " + r[2]['name'] + ", located at " + r[2]['location'] + "." 
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': return_string})



                  

    

""" --- Intents --- """


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'Greeting':
        return say_hi(intent_request)
    elif intent_name == 'ThankYou':
        return say_bye(intent_request)
    elif intent_name == 'SearchFeature':
        return search_feature(intent_request)
    elif intent_name == 'SearchLocation':
        return search_location(intent_request) 
    elif intent_name == 'SearchPrice':
        return search_price(intent_request)
    elif intent_name == 'SearchRest':
        return search_restaurant(intent_request)
        #return dining(intent_request)
    raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    
    #os.environ['TZ'] = 'America/New_York'
    #time.tzset()
    #logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
    
    #m_test()
    #return {
    #    'statusCode': 200,
    #    'body': json.dumps('Hello from Lambda!')
    #}
    
    
# def m_test():
#     sqs = boto3.resource('sqs')
#     queue = sqs.get_queue_by_name(QueueName='cc-assignment2-queue.fifo')
#     print(queue.url)
#     print(queue.attributes.get('DelaySeconds'))
#     location = 'New York'
#     cuisine = 'Chinese'
#     msg_body = {"term":"restaurants", "location":location, "categories":cuisine, "sort_by":'rating', "limit":3, "phone":'+16464009197', "NumberPeople":3, "dinningDate":"05/01/2019", "DinningTime":"22:00"}
#     response = queue.send_message(MessageBody=json.dumps(msg_body), MessageGroupId='MyMessageGroupId1234567890', MessageDeduplicationId='MessageDeduplicationId12345678901')
#     print(response.get('MessageId'))
#     print(response.get('MD5OfMessageBody'))
    
