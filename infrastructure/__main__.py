import json

import pulumi
import pulumi_aws as aws
from pulumi_docker_build  import DockerfileArgs, Image, BuildContextArgs

aws_config = pulumi.Config('aws')
region = aws_config.require('region')
config = pulumi.Config('weather_api')

# TWILIO CONFIG
twilio_account_sid = config.require_secret("TWILIO_ACCOUNT_SID") or ''
twilio_account_sid_param = aws.ssm.Parameter(
    'twilio-account-sid-param',
    type="SecureString",
    value=twilio_account_sid,
    name='/ec2/deployment/credentials/twilio-account-sid-param'
)

twilio_auth_token = config.require_secret("TWILIO_AUTH_TOKEN") or ''
twilio_auth_token_param = aws.ssm.Parameter(
    'twilio-auth-token-param',
    type="SecureString",
    value=twilio_auth_token,
    name='/ec2/deployment/credentials/twilio-auth-token-param'
)

twilio_phone_number = config.require_secret("TWILIO_PHONE_NUMBER") or ''
twilio_phone_number_param = aws.ssm.Parameter(
    'twilio-phone-number-param',
    type="SecureString",
    value=twilio_phone_number,
    name='/ec2/deployment/values/twilio-phone-number-param'
)

to_phone_number = config.require("TO_PHONE_NUMBER") or ''
to_phone_number_param = aws.ssm.Parameter(
    'to-phone-number-param',
    type="String",
    value=to_phone_number,
    name='/ec2/deployment/values/to-phone-number-param'
)

# WEATHER API CONFIG
weather_api_key = config.require_secret("API_KEY_WAPI") or ''
weather_api_key_param = aws.ssm.Parameter(
    'weather-api-key-param',
    type="SecureString",
    value=weather_api_key,
    name='/ec2/deployment/credentials/weather-api-key-param'
)

instance_type = config.get('instance_type') or 't2.micro'
ssh_key_name = config.get('ssh_key_name')

ingress_ssh = aws.ec2.SecurityGroupIngressArgs(
    protocol='tcp',
    from_port=22,
    to_port=22,
    cidr_blocks=['0.0.0.0/0'],
)

egress_all = aws.ec2.SecurityGroupEgressArgs(
    protocol="-1",
    from_port=0,
    to_port=0,
    cidr_blocks=['0.0.0.0/0'],
)

security_group = aws.ec2.SecurityGroup(
    "weather-api-sg",
    description="Habilitar acceso SSH",
    ingress=[ingress_ssh],
    egress=[egress_all],
)

ami = aws.ec2.get_ami(
    most_recent=True,
    owners=["137112412989"],
    filters=[
        {"name": "name", "values": ["al2023-ami-*-x86_64"]}
    ]
)

elastic_ip = aws.ec2.Eip("weather-api-eip")

docker_image = Image(
    "weather-api-image",
    dockerfile=DockerfileArgs(
        location='../weather_api/Dockerfile'
    ),
    context=BuildContextArgs(
        location='../weather_api'
    ),
    push=False
)

ssm_policy = aws.iam.Policy(
    "weather-api-ssm-policy",
    description="Policy to allow access to SSM Parameter Store",
    policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "ssm:GetParameter",
                    "ssm:GetParameters",
                    "ssm:GetParametersByPath"
                ],
                "Resource": "*"
            }
        ]
    })
)

weather_api_instance_role = aws.iam.Role(
    "weather-api-instance-role",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "sts:AssumeRole",
                "Principal": {
                    "Service": "ec2.amazonaws.com"
                },
                "Effect": "Allow",
                "Sid": ""
            }
        ]
    })
)

weather_api_role_policy_attachment = aws.iam.RolePolicyAttachment(
    "weather-api-role-policy-attachment",
    role=weather_api_instance_role.name,
    policy_arn=ssm_policy.arn
)

weather_api_instance_profile = aws.iam.InstanceProfile(
    "weather-api-instance-profile",
    role=weather_api_instance_role.name
)

with open('ec2_user_data.sh', 'r') as user_data_file:
    user_data = user_data_file.read()

ec2_instance = aws.ec2.Instance(
    resource_name='weather-api-ec2',
    instance_type='t2.micro',
    ami=ami.id,
    key_name=ssh_key_name,
    associate_public_ip_address=True,
    vpc_security_group_ids=[security_group.id],
    user_data=user_data,
    iam_instance_profile=weather_api_instance_profile.name,
    root_block_device={
        "volumeSize": 8,
        "volumeType": "gp3",
    },
    tags = {
        "Name": "WeatherApiServer"
    }
)

elastic_ip_association = aws.ec2.EipAssociation(
    'weather-api-eip-association',
    instance_id=ec2_instance.id,
    allocation_id=elastic_ip.id,
)

pulumi.export("instance_id", ec2_instance.id)
pulumi.export("public_ip", ec2_instance.public_ip)
pulumi.export("public_dns", ec2_instance.public_dns)
pulumi.export(
    "connect_command",
    pulumi.Output.concat("ssh -i weather-api.pem ec2-user@", elastic_ip.public_ip),
)
