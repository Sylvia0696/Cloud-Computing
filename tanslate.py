import boto3

def lambda_handler(event, context):
    translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)
    text = event["message"]["word"]
    texts = text.split(',')
    res=[]
    for i in texts:
        result = translate.translate_text(Text=i, SourceLanguageCode="en", TargetLanguageCode="zh")
        res.append(result.get('TranslatedText'))
        
    return {
        "greeting": res
    }
