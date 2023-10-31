import sys
import logging
import pickle
import os
# from face_recognition_util import FaceEncodingsLoader
import json

# from s3Coms import S3FileManager

import os
import logging
import sys

import face_recognition
import pickle
import numpy as np


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
        logger.info(event)

        return 'Hello from AWS Lambda using Python' + sys.version+'))))'+str(event) + '!'