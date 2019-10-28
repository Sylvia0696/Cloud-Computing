import boto3
import json
import pickle
MY_ACCESS_KEY_ID = ''
MY_SECRET_ACCESS_KEY = ''
comprehend = boto3.client(service_name='comprehend', region_name='us-east-1',aws_access_key_id=MY_ACCESS_KEY_ID,
    aws_secret_access_key=MY_SECRET_ACCESS_KEY)
                

directory = "./meta_data/"
res = {}
for filename in os.listdir(directory):
    with open(directory+filename,encoding="utf-8") as json_data:
        data = json.load(json_data) 
        res[filename[4:9]]={}
        res[filename[4:9]]["name"] = data['name']
        res[filename[4:9]]['cuisine'] = data['attributes']['cuisine'][0]
        string=""
        for i in data["ingredientLines"]:
            string += i + " and "
        string=string[:-4]
        res[filename[4:9]]['recipe'] = string

pickle.dump(res,open("food.pickle","wb"))

sentiment = {}
count = 0
for i in review_words:
    print(count)
    count+=1
    sentiment[i]=[]
    for j in review_words[i]:
        tmp_sen = comprehend.detect_sentiment(Text=j, LanguageCode='en')
        if tmp_sen["Sentiment"] != "NEUTRAL":
            sentiment[i].append(j)
