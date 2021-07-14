# This lambda funcyion list the instance id that will be used by funcyion start and stop ec2
# fill the doNotRetreive vector with the Name of the machines to exclude from start up and shutdown. if the excluded machines are already running or stop their state will no change

import json
import boto3
ec2 = boto3.resource('ec2')

scope = ['agonisterion','AgonisterionInfrstructure','Veracode','FDG']

# uncomment the following line to exclude instances
doNotRetreive = ['mpr-api-0.0.47','TestApp','mpr-admin-0.0.47','EXTPROXY-NGINX','mysql-shared-instance','Router','Dns','mailServerAgonisterion','BurpAgentA', 'BurpAgentB', 'BurpAgentC', 'BurpProxy', 'BurpEnterpriseWebserver', 'win2012r2_exams','BurpEndpointChecker','RC_test','DefectDojo18', 'win2012r2_exams', 'ec2_candidates_env_windows2012_oracle', 'ec2_candidates_env_threat-hunter-b', 'ec2_candidates_env_threat-hunter-a', 'ec2_candidates_env_openvpnserver', 'ec2_candidates_env_mpr-mysql', 'ec2_candidates_env_mpr-api-0.0.47', 'ec2_candidates_env_mpr-admin-0.0.47', 'ec2_candidates_env_debianjump', 'BurpCollab', 'BurpTeams']

def lambda_handler(event, context):
    # TODO implement
    filters = [{
        'Name': 'tag:Scope',
        'Values': scope # the Scopes that will be retreived
       }]
    exclusion = [{
        'Name': 'tag:Scope',
        'Values': scope
        },
        {
            'Name': 'tag:Name',
            #'Values': ['mpr-api-0.0.47','testApp','mpr-admin-0.0.47','EXTPROXY-NGINX','mysql-shared-instance','Router','Dns','mailServerAgonisterion'] 
            'Values': doNotRetreive
        }
   ]

    instances = ec2.instances.filter(Filters=filters)
    instancestoexclude = ec2.instances.filter(Filters=exclusion)
    
    excluded =  [instance.id for instance in instancestoexclude]
    print excluded
    instances = [instance for instance in instances if instance.id not in excluded]
    
    ids=[instance.id for instance in instances]

    if len(instances) > 0:
        for i in instances:
            buf=""+i.id
            for tag in i.tags:
                if tag['Key'] == 'Name':
                    buf+=" "+tag['Value']
            print buf
    else:
        print("none found")
    return ids
   # return {
   #     "statusCode": 200,
    #    "body": json.dumps('Hello from Lambda!')
   # }

