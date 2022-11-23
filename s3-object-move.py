import json
import boto3
from datetime import date

def lambda_handler(event, context):
    # TODO implement
    date_buckets = [] 
    s3_client = boto3.client('s3')

    #get all possible object dates from tierpoint bucket 
    for key in s3_client.list_objects(Bucket='tierpoint')['Contents']:
        date_buckets.append(str(key['LastModified'])[:10])
        date_buckets = list(set(date_buckets))

    #create date buckets 
    for i in date_buckets:
        if not bucket_check(s3_client, i):
            s3_client.create_bucket(Bucket=i)
   
    #start moving objects into appropriate bucket 
    for key in s3_client.list_objects(Bucket='tierpoint')['Contents']:
        for i in date_buckets: 
            some_date = str(key['LastModified'])[:10]
            if i == some_date:
                res = s3_client.copy_object(Bucket=i, CopySource=str('tierpoint/' + key['Key']), Key=key['Key'])              
                if res is not None:
                    s3_client.delete_object(Bucket='tierpoint', Key=key['Key']) 
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def bucket_check(s3_client, bucket_name):
    already_exists = False
    res = s3_client.list_buckets()
    for r in res['Buckets']:
        if r == bucket_name:
            already_exists = True
            
    return already_exists
