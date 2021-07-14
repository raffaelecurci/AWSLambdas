import boto3
import json
from datetime import datetime
# Enter the region your instances are in. Include only the region without specifying Availability Zone; e.g., 'us-east-1'
region = 'eu-west-1'

def lambda_handler(event, context):
    msg = {"key":"new_invocation", "at": ""+(datetime.now()).isoformat()+""}
    lambda_client = boto3.client('lambda')
    invoke_response = lambda_client.invoke(FunctionName="getInstancesTagList",
                                           InvocationType='RequestResponse',
                                           Payload=json.dumps(msg))
    instances=json.loads(invoke_response['Payload'].read())
    ec2 = boto3.client('ec2', region_name=region)
    #Fast code to do not remove skedler ecs instance. Remove when POC finishes
    if os.environ['ECS_SKEDLER'] and 'i-0a88c96c74d0bed28' in instances:
        instances.remove('i-0a88c96c74d0bed28')
    ec2.stop_instances(InstanceIds=instances)
    print 'stopped your instances: ' + str(instances)
