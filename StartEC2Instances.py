import boto3
import json
from datetime import datetime
# Enter the region your instances are in. Include only the region without specifying Availability Zone; e.g.; 'us-east-1'
region = 'eu-west-1'

def lambda_handler(event, context):
    msg = {"key":"new_invocation", "at": ""+(datetime.now()).isoformat()+""}
    lambda_client = boto3.client('lambda')
    invoke_response = lambda_client.invoke(FunctionName="getInstancesTagList",
                                           InvocationType='RequestResponse',
                                           Payload=json.dumps(msg))
    instances=json.loads(invoke_response['Payload'].read())
    #print invoke_response['Payload'].read()
    ec2 = boto3.client('ec2', region_name=region)
    ec2.start_instances(InstanceIds=instances)
    print 'started your instances: ' + str(instances)
