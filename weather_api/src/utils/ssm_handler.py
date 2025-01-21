import os
import boto3


class SsmHandler:
    def __init__(self, param_lists, region_name=None):
        self.smm_client = boto3.client('ssm', region_name=region_name or 'us-east-1')
        self.param_lists = param_lists

    def perform(self):
        result = []
        for param, env_name in self.param_lists['to_decrypt']:
            value = self.decrypt_ssm_patameter(param)
            result.append((env_name, value))

        for param, env_name in self.param_lists['plain']:
            value = self.plain_ssm_parameter(param)
            result.append((env_name, value))

        return result

    def decrypt_ssm_patameter(self, parameter_name):
        response = self.smm_client.get_parameter(
            Name=parameter_name,
            WithDecryption=True
        )

        return response['Parameter']['Value']

    def plain_ssm_parameter(self, parameter_name):
        response = self.smm_client.get_parameter(Name=parameter_name)

        return response['Parameter']['Value']


def assign_project_env_vars(param_lists):
    ssm_vars = SsmHandler(param_lists)
    envs = ssm_vars.perform()
    for env_name, env_value in envs:
        os.environ[env_name] = env_value
