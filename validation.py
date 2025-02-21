import json
import sys
import boto3
from time import sleep

# Mock EC2 response
def mock_describe_instances(instance_id):
    # Simulating a response for an EC2 instance
    return {
        'Reservations': [{
            'Instances': [{
                'InstanceId': instance_id,
                'State': {'Name': 'running'},
                'PublicIpAddress': '203.0.113.25',  # Random public IP
            }]
        }]
    }

# Mock ELB response
def mock_describe_load_balancers(load_balancer_name):
    # Simulating a response for an ALB
    return {
        'LoadBalancers': [{
            'DNSName': f'{load_balancer_name}-dns-name.us-east-1.elb.amazonaws.com'  # Random DNS name
        }]
    }

#taking data from aws using boto3
# ec2_client = boto3.client('ec2', region_name='us-east-1')
# elb_client = boto3.client('elbv2', region_name='us-east-1')

# Mock ec2 and lb client methods
ec2_client = {'describe_instances': mock_describe_instances}
elb_client = {'describe_load_balancers': mock_describe_load_balancers}

def get_ec2_instance_details(instance_id):
    try:
        response = ec2_client['describe_instances'](instance_id)
        instance = response['Reservations'][0]['Instances'][0]
        
        # getting instace details
        instance_state = instance['State']['Name']
        public_ip = instance.get('PublicIpAddress', 'N/A')  # Public IP might be None initially
        
        # waiting until the ec2 gets a public ip 
        while instance_state != 'running' or public_ip == 'N/A':
            print("Waiting for EC2 instance to be in running state and have a public IP...")
            sleep(10)
            response = ec2_client['describe_instances'](instance_id)
            instance = response['Reservations'][0]['Instances'][0]
            instance_state = instance['State']['Name']
            public_ip = instance.get('PublicIpAddress', 'N/A')
        
        return instance_id, instance_state, public_ip
    except Exception as e:
        print(f"Error fetching EC2 details: {e}")
        sys.exit(1)

# getting lb details
def get_alb_details(load_balancer_name):
    try:
        response = elb_client['describe_load_balancers'](load_balancer_name)
        alb = response['LoadBalancers'][0]
        
        #getting dns name from the lb 
        load_balancer_dns = alb['DNSName']
        return load_balancer_dns
    except Exception as e:
        print(f"Error fetching ALB details: {e}")
        sys.exit(1)

#input data that being used to get info from aws
instance_id_from_terraform = 'i-0123456789abcdef1'  # fake id to mock 
load_balancer_name_from_terraform = 'gal-lb-2'

# getting ec2 info
instance_id, instance_state, public_ip = get_ec2_instance_details(instance_id_from_terraform)

# getting lb info
load_balancer_dns = get_alb_details(load_balancer_name_from_terraform)

# data for verification
verification_data = {
    "instance_id": instance_id,
    "instance_state": instance_state,
    "public_ip": public_ip,
    "load_balancer_dns": load_balancer_dns
}

# save the data to a JSON file
with open('aws_validation.json', 'w') as f:
    json.dump(verification_data, f, indent=4)

print("Verification data has been saved to aws_validation.json.")
