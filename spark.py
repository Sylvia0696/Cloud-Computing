import pyspark
from pyspark import SparkContext, SparkConf
import pickle

conf = SparkConf().setAppName("project")
sc = SparkContext(conf = conf)

contentRDD =sc.textFile("try.txt")

nonempty_lines = contentRDD.filter(lambda x: len(x) > 0)

words = nonempty_lines.flatMap(lambda x: x.split(' '))

filtered_words = words.map(lambda x:x.replace("\\n"," "))
filtered_words = filtered_words.map(lambda x:x.replace("!",""))
filtered_words = filtered_words.map(lambda x:x.replace(".",""))
filtered_words = filtered_words.map(lambda x:x.replace(":",""))
filtered_words = filtered_words.map(lambda x:x.replace("-",""))
filtered_words = filtered_words.map(lambda x:x.replace("*",""))
filtered_words = filtered_words.map(lambda x:x.replace("~",""))
final_words = filtered_words.flatMap(lambda x: x.split(' '))
final_words_filtered = final_words.filter(lambda x: x != '')
final_words_filtered = final_words_filtered.filter(lambda x: len(x)>2)

data = pickle.load(open("reviews.pickle", "rb" ))
directory="./txt_data/"
review_words={}
error=[]
for i in data:
    try:
        contentRDD =sc.textFile(directory+i+".txt")
        nonempty_lines = contentRDD.filter(lambda x: len(x) > 0)
        words = nonempty_lines.flatMap(lambda x: x.split(' '))
        filtered_words = words.map(lambda x:x.replace("\\n"," "))
        filtered_words = filtered_words.map(lambda x:x.replace("!",""))
        filtered_words = filtered_words.map(lambda x:x.replace(".",""))
        filtered_words = filtered_words.map(lambda x:x.replace(":",""))
        filtered_words = filtered_words.map(lambda x:x.replace("-",""))
        filtered_words = filtered_words.map(lambda x:x.replace("*",""))
        filtered_words = filtered_words.map(lambda x:x.replace("~",""))
        final_words = filtered_words.flatMap(lambda x: x.split(' '))
        final_words_filtered = final_words.filter(lambda x: x != '')
        final_words_filtered = final_words_filtered.filter(lambda x: len(x)>2)
        wordcount = final_words_filtered.map(lambda x:(x,1)).reduceByKey(lambda x,y: x+y).map(lambda x: (x[1], x[0])).sortByKey(False)
        review_words[i]=[]
        for word in wordcount.collect():
            review_words[i].append(word[1])
    except:
        error.append(i)
#loading data and sort data
pickle.dump(review_words,open("review_words.pickle","wb"))
bus_data = pickle.load(open('business.pickle','rb'))

final_res = {}
for i in bus_data:
    final_res[i] = bus_data[i]
    temp_emotion = ""
    for j in sentiment[i]:
        temp_emotion += j + ","
    final_res[i]['feature'] = temp_emotion
