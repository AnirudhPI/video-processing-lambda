import requests
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, time
import time
from handler import lambda_handler

# MicroCeph API endpoint to list files in the bucket
MICROCEPH_API_URL = 'http://microceph.example.com/api/list-files'
BUCKET_NAME = 'mybucket'

# Variable to store the last upload time
last_upload_time = datetime.min
'''
def get_file_list():
    """ Fetch the list of files from MicroCeph bucket. """
    response = requests.get(f"{MICROCEPH_API_URL}?bucket={BUCKET_NAME}")
    if response.status_code == 200:
        return response.json()  # Assuming the API returns a list of file info
    else:
        raise Exception("Failed to list files from MicroCeph")
'''

def find_new_uploads(files):
    """ Find new files based on the last upload time. """
    global last_upload_time
    new_files = []
    most_recent_upload = last_upload_time

    for file in files:
        upload_time = datetime.fromisoformat(file['upload_time'])  # Assuming ISO format

        if upload_time > last_upload_time:
            new_files.append(file['name'])
            if upload_time > most_recent_upload:
                most_recent_upload = upload_time

    last_upload_time = most_recent_upload
    return new_files
'''
def handle(req):
    files = get_file_list()
    new_uploads = find_new_uploads(files)
    return new_uploads
'''
def list_keys_in_bucket(s3_client, bucket_name, latest_time):
    """
    List all keys in an S3 bucket along with their last modified timestamps.

    :param s3_client: Boto3 S3 client
    :param bucket_name: Name of the S3 bucket
    :return: List of tuples containing the key and its last modified timestamp
    """
    max_m=latest_time
    try:
        new = []
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            for item in response['Contents']:
                if int(item['LastModified'].timestamp()) > latest_time:
                    new.append((item['Key'], int(item['LastModified'].timestamp())))
                    if max_m < int(item['LastModified'].timestamp()):
                        max_m = int(item['LastModified'].timestamp())
            latest_time = max_m
            return new, latest_time
        else:
            return new, 0
        
    except ClientError as e:
        return str(e)
    
endpoint_url = 'http://54.196.19.249:8000/'
access_key = 'AKIA25MVWGGJN7JUPP5K'
secret_key = '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'
# Initialize the S3 client
s3_client = boto3.client('s3', endpoint_url=endpoint_url, aws_access_key_id=access_key,
                              aws_secret_access_key=secret_key, region_name='us-east-1')

# Specify your bucket name
bucket_name = 'inputbucket-cloudcomputing2'
    
if __name__ == "__main__":

    # List keys in the specified bucket
    last_tm = 0
    # keys, last_tm = list_keys_in_bucket(s3_client, bucket_name, last_tm)
    # print(keys, last_tm)
    while True:
        
        keys, last_tm = list_keys_in_bucket(s3_client, bucket_name, last_tm)
        print(keys, last_tm)
        for k,t in keys:
            print(f"running openfass for {k}")
            event = {
                "Records": [
                    {
                        "s3": 
                        {
                            "object": {
                                "key": k
                            }
                        }
                    }   
                ]
            }

            lambda_handler(event)

            # response = requests.post(url="http://192.168.49.2:31112/function/facerecog-docker", data=event)
            # if response.status_code == 200:
            #     print(response.json())  # Assuming the API returns a list of filenames
            # else:
            #     raise Exception("url failed")
        #lambda_handler(event=event, context='aaa')
            
        time.sleep(2)