import boto

'''
Create an access key programatically
(referenced: http://boto3.readthedocs.io/en/latest/guide/iam-example-managing-access-keys.html
https://boto3.readthedocs.io/en/latest/reference/services/iam.html#IAM.Client.create_access_key)
'''
iam = boto.client('iam')
response = iam.create_access_key()

'''
Create a connection. Specify the region where you want to
setup ec2 along with your security credentials
'''

conn = boto.ec2.connect_to_region("us-west-2",
		aws_access_key_id = response['AccessKey']['AccessKeyId'],
		aws_secret_access_key = response['AccessKey']['SecretAccessKey'])

'''
Create a security group.
https://boto3.readthedocs.io/en/latest/reference/services/ec2.html#EC2.Client.create_security_group
'''
client = boto.client('ec2')
response = client.create_security_group(
    Description='minihw1',
    GroupName='minihw1',
    #VpcId='string',
    DryRun=False
)
security_grp = response['GroupId']

response = ec2.authorize_security_group_ingress(
        GroupId=security_grp,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ])

#@TODO: get key pair name
response = ec2.create_key_pair(KeyName='KEY_PAIR_NAME')
'''
Launch your ec2 instance. This requires ami image id and instance type.
Refer to the AWS documentation for details. You need to setup your
key-pair and security group before launching.
'''
conn.run_instances(
        '<ami-image-id>', #that depends on like, ubuntu64 etc
        key_name = 'KEY_PAIR_NAME', #from ec2
        instance_type = 't2.micro',
        security_groups = [security_grp])


#@TODO: parse returned response (see below)
'''
You need to parse the returned response to print the following:
 - external IP address
 - which region instance was created
 - instance ID

Do remember to use the correct key-pair and the security group with the
correct access settings to make sure you can SSH into these instances.

Validate that your instance was created successfully by SSHing into the instance.
Screenshot

'''


'''
Stop instance
'''

conn.stop_instances(instance_ids=['instance-id'])


'''
Terminate instance
'''
conn.terminate_instances(instance_ids=['instance-id'])
