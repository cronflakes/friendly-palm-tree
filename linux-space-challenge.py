import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    db = boto3.client('dynamodb') 
    ec2 = boto3.client('ec2') 
    iam = boto3.client('iam')
    
    inst_profile_name = 'linux-challenge-1-profile'
    role_name = 'linux-challenge-1-role'
    cleanIAMRolesAndProfiles(iam, role_name, inst_profile_name)
    
    policy = { 
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "ec2.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
   
    inst_profile = iam.create_instance_profile(InstanceProfileName=inst_profile_name)
    role = iam.create_role(RoleName=role_name, AssumeRolePolicyDocument=json.dumps(policy))
    #iam.add_role_to_instance_profile(InstanceProfileName=inst_profile_name, RoleName=role_name)
    iam.put_role_policy(RoleName='linux-challenge-1-role', PolicyName='linux-challenge-1-policy', PolicyDocument=policy)
  
    ec2_inst = ec2.run_instances(ImageId='ami-0abe861b63f2b08bb', InstanceType='t2.micro', MinCount=1, MaxCount=1, IamInstanceProfile={'Name': inst_profile_name})
    inst_id = str(ec2_inst['Instances'][0]['InstanceId'])
    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=[inst_id], Filters=[{ "Name":"instance-state-code", "Values": ["running"] }])
    
    
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
    

def cleanIAMRolesAndProfiles(iam, role, profile):
    try:
        iam.delete_instance_profile(InstanceProfileName=profile)
        print('deleted instance profile')
    except iam.exceptions.NoSuchEntityException:
        #instance profile doesn't exist
        pass 
    except iam.exceptions.DeleteConflictException as e:
        print(e)
    
    try:
        iam.delete_role(RoleName=role)
        print('deleted role')
    except iam.exceptions.NoSuchEntityException:
        #role doesnt exist
        pass 
    except iam.exceptions.DeleteConflictException as e:
        print(e)
        #must remove role from instance profiles
        #doing this on the terminal was so much faster
        #aws iam remove-role-from-instance-profile --instance-profile-name linux-challenge-5-profile --role-name linux-challenge-1-role 
