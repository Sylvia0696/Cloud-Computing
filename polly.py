"""Getting Started Example for Python 2.7+/3.3+"""
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
from io import BytesIO
import boto3

prefix = 'ml'

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).
# session = Session(profile_name="default")
polly = boto3.client("polly")
def lambda_handler(event, context):
    try:
        # Request speech synthesis
        text = "Hello world!"
        response = polly.synthesize_speech(Text=text, OutputFormat="mp3",
                                            VoiceId="Joanna")
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        sys.exit(-1)
    
    # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important as the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
        with closing(response["AudioStream"]) as stream:
            # output = os.path.join(gettempdir(), "speech.mp3")
    
            try:
                # Open a file for writing the output as a binary stream
                s3 = boto3.resource('s3')
                bucket = s3.Bucket('pow8518')
                path_test = '/tmp/output'
                key = 'sound.mp3'
                with open(path_test, 'wb') as f:
                    f.write(stream.read())
                    bucket.upload_file(path_test, key)
                
                s3_connection = boto.connect_s3()
                key = boto.s3.key.Key(bucket, 'sound.mp3')
                with open('sound.mp3') as f:
                    key.write(stream.read())
                    
                s3 = boto3.client('s3')
                FILE_1_key = "FILE_1.mp3"
                FILE_1_path = "s3://{}/{}/{}".format(bucket, prefix, FILE_1_key)
                s3 = s3fs.S3FileSystem(anon=False)
                with s3.open(FILE_1_path, 'wb') as f:
                    f.write(stream.read())
    
                fileobj = BytesIO(stream.read())
    
                s3.upload_fileobj(fileobj, 'mybucket', 'mykey')
                with open("speech.mp3", "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
                sys.exit(-1)
    
    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        sys.exit(-1)
        
    return("!!!")
    
    
    
    
    
    # Play the audio using the platform's default player
    if sys.platform == "win32":
        os.startfile(output)
    else:
        # the following works on Mac and Linux. (Darwin = mac, xdg-open = linux).
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, output])