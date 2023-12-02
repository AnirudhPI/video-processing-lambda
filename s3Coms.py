import boto3


aws_access_key_id = 'AKIA25MVWGGJN7JUPP5K'
aws_secret_access_key = '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'
aws_region = 'us-east-1' 


endpoint_url = 'http://54.196.19.249:8000/'
access_key = 'AKIA25MVWGGJN7JUPP5K'
secret_key = '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'


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

# Example usage:
if __name__ == "__main__":
    bucket_name = "inputbucket-cloudcomputing2"
    s3_manager = S3FileManager(bucket_name)
    
    # Upload an image to S3
    # s3_manager.upload_image("image.jpg", "local_image.jpg")

    # Upload text content to S3
    # s3_manager.upload_text("text_fppo.txt", "This is a text file.")

    # Copy an image from S3 to a local file
    # s3_manager.upload_image("test_3.mp4", "test_0.mp4")
    # s3_manager.copy_video_to_file("test_0.mp4", "test_0.mp4")


    s3_output = S3FileManager("outputbucket-cloudcomputing2")
    s3_output.read_s3_object("test_0")

