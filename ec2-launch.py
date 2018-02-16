import boto3
import boto3.ec2
import boto.ec2

keyname = "MY_KEY_NAME14" #set as global
sgn = 'minihw15'

'''
Create a connection. Specify the region where you want to
setup ec2 along with your security credentials
boto automatically grabs credentials from my aws config file
'''

conn = boto.ec2.connect_to_region("us-east-1")

'''
Create a security group.
https://boto3.readthedocs.io/en/latest/reference/services/ec2.html#EC2.Client.create_security_group
'''
client = boto3.client('ec2')
response = client.create_security_group(
    Description='minihw1',
    GroupName=sgn,
    #VpcId='string',
    DryRun=False
)
security_grp = response['GroupId']

response = client.authorize_security_group_ingress(
        GroupId=security_grp,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22
             #'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
			 }
        ])


'''
create ec2 key pair and store in a .pem file for SSH
'''
response = conn.create_key_pair(key_name=keyname)
response.save("./")

'''
Launch your ec2 instance. This requires ami image id and instance type.
Refer to the AWS documentation for details. You need to setup your
key-pair and security group before launching.
'''
response = conn.run_instances(
        'ami-7ea24a17', #centos
        key_name = keyname, #from ec2
        instance_type = 't2.micro',
        security_groups = [sgn])
#print response

#@TODO: parse returned response (see below)
'''
You need to parse the returned response to print the following:
 - external IP address
 - which region instance was created
 - instance ID
'''
resp = response.instances[0]
#print dir(resp)

iid = resp.id
print "external IP address: " + resp.ip_address
print "region: " + resp.region
print "instance ID: " + iid

'''
Do remember to use the correct key-pair and the security group with the
correct access settings to make sure you can SSH into these instances.

Validate that your instance was created successfully by SSHing into the instance.
Screenshot

'''
str = ''
while (str != 'STOP' and str != 'STOP\n'):
	str = raw_input('type STOP to stop')


'''
Stop instance
'''

conn.stop_instances(instance_ids=[iid])


'''
Terminate instance
'''
conn.terminate_instances(instance_ids=[iid])
