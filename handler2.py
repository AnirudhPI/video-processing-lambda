import sys
def handler(event, context):
    print(event)
    return 'Hello from AWS Lambda using Python' + sys.version + '!'
