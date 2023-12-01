import boto3
import json


aws_access_key_id = 'AKIA25MVWGGJN7JUPP5K'
aws_secret_access_key = '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'
aws_region = 'us-east-1' 


# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb', 
							region_name=aws_region,
							aws_access_key_id=aws_access_key_id, 
                            aws_secret_access_key=aws_secret_access_key)

# Specify the table name
table_name = 'Students'

# Load the student data from the JSON file
with open('student_data.json', 'r') as json_file:
    student_data = json.load(json_file)

# Get a reference to the DynamoDB table
table = dynamodb.Table(table_name)

# Iterate through the student data and put each item into the DynamoDB table
for student in student_data:
    response = table.put_item(Item=student)
    print(f"Added student: {student['id']}")