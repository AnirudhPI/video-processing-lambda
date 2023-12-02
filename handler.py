
import cv2
import os
import boto3
import face_recognition
import pickle
import os
# from face_recognition_util import FaceEncodingsLoader
import json

# from s3Coms import S3FileManager

import os
import logging
import sys


import pickle
import numpy as np


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

logger = logging.getLogger()
logger.setLevel(logging.INFO)



# s3 = boto3_client('s3')
# dynamodb = boto3.resource('dynamodb')


input_bucket = "inputbucket-cloudcomputing2"
output_bucket = "outputbucket-cloudcomputing2"

endpoint_url = 'http://54.196.19.249:8000/'
access_key = 'AKIA25MVWGGJN7JUPP5K'
secret_key = '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'


aws_access_key_id = 'AKIA25MVWGGJN7JUPP5K'
aws_secret_access_key = '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'
aws_region = 'us-east-1' 



class FaceEncodingsLoader:
    def __init__(self, encoding_file):
        self.encodings = self.load_encodings(encoding_file)

    def load_encodings(self, filename):
        try:
            with open(filename, "rb") as file:
                encodings = pickle.load(file)
            return encodings
        except Exception as e:
            raise ValueError(f"Failed to load encodings from {filename}: {str(e)}")

    def get_encodings(self):
        return self.encodings

    def find_best_match(self, known_encodings, unknown_image_path,names, threshold=0.6):
        """
        Compares an unknown face image to a list of known face encodings and returns the best match.
        
        :param known_encodings: List of known face encodings (numpy arrays).
        :param unknown_image_path: Path to the unknown image for comparison.
        :param threshold: Similarity threshold for considering a match (default is 0.6).
        :return: Name or identifier of the best match, or None if no match is found.
        """
        # Load the unknown image
        print(unknown_image_path)
        unknown_image = face_recognition.load_image_file(unknown_image_path)

        # Encode the faces in the unknown image
        face_locations = face_recognition.face_locations(unknown_image)
        unknown_encodings = face_recognition.face_encodings(unknown_image, face_locations)

        # unknown_encodings = face_recognition.face_encodings(unknown_image)

        if not unknown_encodings:
            return None  # No faces found in the unknown image.

        # Compare the unknown face encodings to the list of known encodings
        matches = face_recognition.compare_faces(known_encodings, unknown_encodings[0], tolerance=threshold)

        face_distances = face_recognition.face_distance(known_encodings, unknown_encodings[0])
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = names[best_match_index]
            return name
        else:
            return "unknown face"
        



class S3FileManager:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        session = boto3.session.Session()
        self.s3 = session.client(
            service_name='s3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
                )
        

        # self.s3 = boto3.client('s3', ,region_name=aws_region, 
        #                        aws_access_key_id=aws_access_key_id, 
        #                        aws_secret_access_key=aws_secret_access_key)

    def upload_image(self, key, image_file):
        """
        Upload an image file to S3.

        Args:
            key (str): The object key (S3 filename).
            image_file (str): The local path to the image file.
        """
        self.s3.upload_file(image_file, self.bucket_name, key)

    def upload_text(self, key, text):
        """
        Upload text content to S3.

        Args:
            key (str): The object key (S3 filename).
            text (str): The text content to upload.
        """
        self.s3.put_object(Bucket=self.bucket_name, Key=key, Body=text)

    def copy_video_to_file(self, key, file_path):
        """
        Copy an image from S3 to a local file.

        Args:
            key (str): The object key (S3 filename).
            file_path (str): The local path where the image should be copied.
        """
        self.s3.download_file(self.bucket_name, key, file_path)

    def get_object(self, object_key):
        return self.s3.get_object(Bucket=self.bucket_name, Key=object_key)

    def list_all_objects(self):
        return self.s3.list_objects(Bucket=self.bucket_name)
    
    def read_s3_object(self, object_key):
        print(f"retrieving {object_key} from {bucket_name}")
        try:
            # Get the object from S3
            response = self.s3.get_object(Bucket=self.bucket_name, Key=object_key)

            content = response['Body'].read().decode('utf-8')
            print(content)

        except Exception as e:
            print(f"Error reading S3 object: {e}")


s3_input = S3FileManager(input_bucket)
s3_results = S3FileManager(output_bucket)




def save_frames(video_file_path, folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    cap = cv2.VideoCapture(video_file_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        output_path = os.path.join(folder_name, f"image-{frame_count:03d}.jpeg")
        cv2.imwrite(output_path, frame)

        frame_count += 1

    cap.release()
    print(f"Total frames saved: {frame_count}")


def handle(event):
	print("using lamba_handler")
	return lambda_handler(event)

def lambda_handler(event):
	# Get the S3 bucket and object information from the S3 event

	print(event)

	logger.info('## Function triggered')
	s3_event = event['Records'][0]['s3']
	object_key = s3_event['object']['key']

	downloaded_video_path = "/tmp/"
	video_file_path = downloaded_video_path+object_key
	folder_path = video_file_path.split(".")[0]
	s3_input.copy_video_to_file(object_key, video_file_path)
	logger.info(f'video {object_key} downloaded at {video_file_path}')
	logger.info(f"save_frames({video_file_path},{folder_path})")
	save_frames(video_file_path,folder_path)


	
	# unknown face

	encoding_file = "encoding"  # Replace with the path to your encoding file
	encodings_loader = FaceEncodingsLoader(encoding_file)
    
	# Get the loaded encodings
	loaded_encodings = encodings_loader.get_encodings()
	logger.info(f'encodings loaded')


		# List all files in the folder
	files = os.listdir(folder_path)

	results = "unknown face"

	# Process each file one by one
	for file in files:
		file_path = os.path.join(folder_path, file)

		# Check if the item is a file (not a subdirectory)
		if os.path.isfile(file_path):
			logger.info(f"Processing file: {file_path}")

			# print(f"Processing file: {file_path}")

		results  = encodings_loader.find_best_match(loaded_encodings["encoding"],file_path,loaded_encodings["name"])
		if results !=  "unknown face":
			break


	logger.info(f"found result: {results}")
	# aws_region = 'us-east-1'  # Replace with your desired AWS region
	# DynamoDB resource
	dynamodb = boto3.resource('dynamodb', 
							region_name=aws_region,
							aws_access_key_id=aws_access_key_id, 
                            aws_secret_access_key=aws_secret_access_key)

	table_name = 'Students'

	# Specify the column name and the value you want to filter on
	column_name = 'name'
	filter_value = results

	# Retrieve data from DynamoDB where "name" equals "president_obama"
	table = dynamodb.Table(table_name)

	dynamo_response = table.scan(
		FilterExpression=boto3.dynamodb.conditions.Attr(column_name).eq(filter_value)
	)

	response = dynamo_response["Items"][0]

	logger.info(f" response from dynamo {response}")
	final_string = f'{filter_value}, {response["major"]}, {response["year"]}'
	logger.info(f"final string generated: {final_string}")
	s3_results.upload_text(object_key.split(".")[0],final_string)


	print(results)



	# Create a DynamoDB table resource
	# table = dynamodb.Table(table_name)


	# Copy the image from S3 to a local file


	# Search DynamoDB for the record using the filename (object_key)
	# response = table.get_item(
	# 	Key={
	# 		'string': final_string
	# 	}
	# )

	return {
			'statusCode': 200,
			'body': json.dumps(final_string)
		}


event = {
  "Records": [
    {
      "eventVersion": "2.1",
      "eventSource": "aws:s3",
      "awsRegion": "us-east-1",
      "eventTime": "1970-01-01T00:00:00.000Z",
      "eventName": "ObjectCreated:*",
      "s3": {
        "s3SchemaVersion": "1.0",
        "configurationId": "bcca404d-cb99-48f8-a05d-696eacf53c5b",
        "bucket": {
          "name": "inputbucket-cloudcomputing2",
          "ownerIdentity": {
            "principalId": "022286511304"
          },
          "arn": "arn:aws:s3:::inputbucket-cloudcomputing2"
        },
        "object": {
          "key": "test_0.mp4",
          "size": 322560,
          "eTag": "0123456789abcdef0123456789abcdef",
          "sequencer": "0A1B2C3D4E5F678901"
        }
      }
    }
  ]
}

handle(event)