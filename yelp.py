import requests
import json
headers={"Authorization": "Bearer Vv3D0MWqERhHbN7M5C1Wb1tTvsezZeISd8u6T50QI7zxkdzaLXhjQjCdRhiTqR7w1BZtPc722pRAaawBoKjgayUauLDxTV9lzfL12pwUzFVoUmAC-HUZ9s5fc_iCXHYx"}

price = 0
if input_price <= 15:
    price = 1
elif input_price > 15 and input_price <= 30:
    price = 2
elif input_price > 30 and input_price <= 45:
    price = 3
else:
    price = 4
business={}
error=[]
for i in data:
    headers={"Authorization": "Bearer _-P2p2WZZVem_rnxbimYqaVlOFnIVXWPWBuKO9Apzbwxt1gXafizlwu7loOc9SPM9o6KI8WSxEDSYHkkByr-GtuD50Gm8KxqJES3-eNX09RuZayeatP1VRuLk8uCXHYx"}
    params={}
    myResponse = requests.get("https://api.yelp.com/v3/businesses/"+i, headers=headers, params=params)
    r = myResponse.json()
    try:
        business[i]={}
        business[i]['alias'] = r['alias']
        business[i]['name'] = r['name']
        business[i]['image_url'] = r['image_url']
        business[i]['location'] = r['location']
        business[i]['rating'] = r['rating']
        business[i]['price'] = r['price']
        for c in r["categories"][0]:
            business[i]['category']=r["categories"][0][c]
            break
    except:
        error.append(i)

pickle.dump( new_business, open( "business.pickle", "wb" ) )

new_business = {}
for i in business:
    if len(business[i].keys()) == 7:
        new_business[i] = business[i]

for i in range(0,20):
    headers={"Authorization": "Bearer _-P2p2WZZVem_rnxbimYqaVlOFnIVXWPWBuKO9Apzbwxt1gXafizlwu7loOc9SPM9o6KI8WSxEDSYHkkByr-GtuD50Gm8KxqJES3-eNX09RuZayeatP1VRuLk8uCXHYx"}
    params={
            "term":"restaurants",
            "location":"chicago",
            "limit":50,
            "offset":50*i
        }
    myResponse = requests.get("https://api.yelp.com/v3/businesses/search", headers=headers, params=params)
    r = myResponse.json()
    for j in r["businesses"]:
        result.append(j["id"])

file = open('FILE_1.csv', 'r', encoding='utf-8')
csv_reader = csv.reader(file)
next(csv_reader)
for row in csv_reader:
    restaurantID.append(row[0])

clean = set()
for i in range(len(restaurantID)):
    if restaurantID[i] in clean:
        del(restaurantID[i])
    else:
        clean.add(restaurantID[i])

import pickle
pickle.dump( clean, open( "IDs.pickle", "wb" ) )
# favorite_color = pickle.load( open( "IDs.pickle", "rb" ) )
reviews={}
for i in clean:
    myResponse = requests.get("https://api.yelp.com/v3/businesses/"+i+"/reviews", headers=headers, params={})
    r = myResponse.json()
    temp_res=[]
    try:
        for j in r["reviews"]:
            temp_res.append(j["text"])
        reviews[i]=temp_res
    except:
        continue
    