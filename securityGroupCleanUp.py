import boto3
import argparse
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('start')

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2') #You have to change this line based on how you pass AWS credentials and AWS config
    
    sgs = list(ec2.security_groups.all())
    insts = list(ec2.instances.all())
    
    all_sgs = set([sg.id for sg in sgs])
    all_inst_sgs = set([sg['GroupId'] for inst in insts for sg in inst.security_groups])
    
    unused_sgs = all_sgs - all_inst_sgs
    print 'Total SGs:', len(all_sgs)
    print 'SGS attached to instances:', len(all_inst_sgs)
    print 'Orphaned SGs:', len(unused_sgs)
    print 'Unattached SG names:', unused_sgs
    for i in unused_sgs:
        try:
           ec2.SecurityGroup(i).delete()
        except Exception as e:
            print(e)
            print("{0} requires manual remediation.".format(i))
            
    return 0

