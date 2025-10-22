import json
import boto3
import os
from dotenv import load_dotenv

load_dotenv()
# 加载.env文件

def lambda_handler():
    # TODO implement
    s3 = boto3.client("s3")
    bucket = os.environ["dictionary_bucket"]
    key = os.environ["dictionary_file"]
    # print(bucket)
    response = s3.get_object(Bucket=bucket, Key=key)
    file_content = response["Body"].read().decode("utf-8")
    return {"statusCode": 200, "body": json.dumps(file_content)}

print(lambda_handler())
