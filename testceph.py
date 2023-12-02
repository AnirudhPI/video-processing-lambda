import boto3

def upload_file_to_ceph(file_path, bucket_name, object_name):
    # Ceph/RGW endpoint and access keys
    endpoint_url = 'http://54.196.19.249:8000'
    access_key = 'AKIA25MVWGGJN7JUPP5K'
    secret_key = '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'
    
    # Create a session using Ceph credentials
    session = boto3.session.Session()
    s3_client = session.client(
        service_name='s3',
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
    
    # Upload file to the specified bucket and object name
    try:
        extra_args = {'ContentType': 'text/plain'}  # Set the content type based on your file type
        s3_client.upload_file(file_path, bucket_name, object_name, ExtraArgs=extra_args)
        print(f"File '{file_path}' uploaded to '{bucket_name}/{object_name}' successfully.")
    except Exception as e:
        print(f"File upload failed: {e}")

if __name__ == "__main__":
    file_to_upload = 'test_0.mp4'  # Replace with your file path
    bucket_name = 'inputbucket'  # Replace with your bucket name
    object_name = 'test_0.mp4'  # Replace with your desired object name
    upload_file_to_ceph(file_to_upload, bucket_name, object_name)