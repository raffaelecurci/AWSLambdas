import boto3
import json
import time
from datetime import datetime
from pprint import pprint
# Enter the region your instances are in. Include only the region without specifying Availability Zone; e.g.; 'us-east-1'




def lambda_handler(event, context):
    # TODO implement
    region = 'eu-west-1'
    ec2 = boto3.resource('ec2')
    ec2_client = boto3.client('ec2', region_name=region)
    
    
    instances_name_to_manage=['mpr-api-0.0.47','TestApp','mpr-admin-0.0.47','EXTPROXY-NGINX','mysql-shared-instance']
    
    filters = [{
        'Name': 'tag:Name',
        'Values': instances_name_to_manage # the Scopes that will be retreived
       }]
    
    
    #retrieve ids for the instance to manage
    
  
    
    snapShotFilters = [{'Name':'tag:Scope', 'Values':['Interview']}]
    instances = ec2.instances.filter(Filters=filters)
    snapshots = ec2.snapshots.filter(Filters=snapShotFilters)
    
    ist=[]
    for i in instances:
        print i.state
        if i.state['Name'] == 'running':
            #ec2_client.stop_instances(InstanceIds=[i.id])
            #ec2_client.get_waiter('instance_stopped').wait(InstanceIds=[i.id])
            while i.state['Name'] not in ('stopped'):
                time.sleep(2)
                #i.update()
            #print i.state +" "+ i.id
        volumes=[j.id for j in i.volumes.all()]
        name=""
        for tag in i.tags:
            if tag['Key'] == 'Name':
                name=tag['Value']
        volume=''
        if len(volumes)>0:
            volume=volumes[0]
            
        v={'id': i.id, 'name' : name , 'volume' : volume}
        ist.append(v)
    #ec2_client.stop_instances(InstanceIds=ids)
    #print (ist)
    snaps=[]
    for i in snapshots:
        name=""
        for tag in i.tags:
            if tag['Key'] == 'Name':
                name=tag['Value']
        snap={'id': i.id, 'name' : name }
        snaps.append(snap)
    
    snaps4instances=[]
    for i in ist:
        for j in snaps:
            if i['name'] in j['name'] :
            #   print 'snapshot found'
                snaps4instances.append({'id': i['id'], 'name' : i['name'], 'volume': i['volume'], 'id_snap' : j['id'] , 'name_snap' : j['name']})
    
    print snaps4instances
    for i in snaps4instances:
        print i['volume']
        print i['name']
        
        ec2_client.detach_volume(VolumeId=i['volume'], Device='/dev/sda1',InstanceId=i['id'])
        volume = ec2.create_volume(SnapshotId=i['id_snap'], AvailabilityZone='eu-west-1c')
        volume.create_tags(Tags=[{'Key':'Name','Value': i['name']+"CANDIDATE"}])
        
        ec2_client.get_waiter('volume_available').wait(VolumeIds=[volume.id])
        
        response=ec2_client.attach_volume(VolumeId=volume.id, Device='/dev/sda1',InstanceId=i['id'])
        #pprint(response)
        
        oldVolume=ec2.Volume(i['volume'])
        
        oldVolume.create_tags(Tags=[{'Key':'Name','Value': i['name']+"CANDIDATE_OLD"}])
        
        i['volume']=volume.id
        #print oldVolume.id
        #print i['volume']
        #break
    
    
    instance2start=[{'Name':'tag:Name', 'Values':['mysql-shared-instance']}]
    toStart = ec2.instances.filter(Filters=instance2start)
    id=[j.id for j in toStart]
    ec2_client.start_instances(InstanceIds=id)
    ec2_client.get_waiter('instance_running').wait(InstanceIds=id)
    
    instance2start=[{'Name':'tag:Name', 'Values':['mpr-api-0.0.47']}]
    toStart = ec2.instances.filter(Filters=instance2start)
    id=[j.id for j in toStart]
    ec2_client.start_instances(InstanceIds=id)
    ec2_client.get_waiter('instance_running').wait(InstanceIds=id)
    
    instance2start=[{'Name':'tag:Name', 'Values':['mpr-admin-0.0.47']}]
    toStart = ec2.instances.filter(Filters=instance2start)
    id=[j.id for j in toStart]
    ec2_client.start_instances(InstanceIds=id)
    ec2_client.get_waiter('instance_running').wait(InstanceIds=id)
    
    instance2start=[{'Name':'tag:Name', 'Values':['EXTPROXY-NGINX']}]
    toStart = ec2.instances.filter(Filters=instance2start)
    id=[j.id for j in toStart]
    ec2_client.start_instances(InstanceIds=id)
    ec2_client.get_waiter('instance_running').wait(InstanceIds=id)
    
    instance2start=[{'Name':'tag:Name', 'Values':['TestApp']}]
    toStart = ec2.instances.filter(Filters=instance2start)
    id=[j.id for j in toStart]
    ec2_client.start_instances(InstanceIds=id)
    
    
    
    
    
    
    #stop the ec2
    #ec2_client = boto3.client('ec2', region_name=region)
    #ec2_client.stop_instances(InstanceIds=ids)
    #print 'started your instances: ' + str(instances)
    
    
    #print ids
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

