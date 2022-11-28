import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    db = boto3.client('dynamodb') 
    ec2 = boto3.client('ec2') 
   
    ec2_inst = ec2.run_instances(ImageId='ami-04f6621d886139d05', InstanceType='t2.micro', MinCount=1, MaxCount=1) 
    
    res = db.scan(TableName='linux-challenge')
    #print(res['Items'][0]['date']['S']) 
    creds = getCredsFromDB(res)
    print(creds)
            
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def getCredsFromDB(res):
    needed_query = '' 
    current_latest = 0 
    for i in res['Items']:
        latest = int(i['date']['S'])
        if(latest > current_latest):
            current_latest = latest
            needed_query = i     
            
    return needed_query['password']['S']
