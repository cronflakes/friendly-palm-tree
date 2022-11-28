import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    db = boto3.client('dynamodb') 
    ec2 = boto3.client('ec2') 
   
    ec2_inst = ec2.start_instances(InstanceIds=['i-09ae6b7d1f332d4c6'],)
    ec2_inst.wait_until_running()
    
    #this is failing because the ec2 instances may have a status of running, but the OS may not be fully booted (and the systemd service may not even be fully running either)
    #check whether boto3 has an API for checking systemd services after lunch
    
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
