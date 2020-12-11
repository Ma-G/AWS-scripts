import boto3
import os
from botocore.config import Config

# This script copies (creates or/and updates) parameters to Parameter Store
# from one region to another - var copy_to_region
# It also replaces the suffix of the parameter (var stage) with a new one (var new_stage)
  

# stage I copy from
stage = "prod"
# stage I copy to
new_stage = "hotfix"
# region I copy to
copy_to_region = "eu-central-1"


client = boto3.client('ssm')
access_key_id=os.getenv('AWS_ACCESS_KEY_ID')
secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')

suffix_to_rm = len(stage.strip())

def describe_params():
    parameters = client.describe_parameters()
    results = parameters["Parameters"]
    while "NextToken" in parameters:
        parameters = client.describe_parameters(NextToken=parameters['NextToken'])
        results.extend(parameters["Parameters"])
    return results

def get_params_name_value_type(record):
    param_name = record['Name']
    params_with_values = client.get_parameter(
    Name = param_name,
    WithDecryption = True
    )
    param_name = params_with_values['Parameter']['Name']
    param_value = params_with_values['Parameter']['Value']
    param_type = params_with_values['Parameter']['Type']
    return param_name, param_value, param_type



def change_param_name_suffix(param_name):
    param_name_wo_stage = param_name[:-suffix_to_rm]
    param_name_new_stage= param_name_wo_stage + new_stage
    return param_name_new_stage





def put_params_in_ps(param_name, param_value, param_type, aws_region):
    my_config = Config(
    region_name = aws_region,
    )

    client = boto3.client('ssm', config=my_config)
    client.put_parameter(
        Name = param_name,
        Value = param_value,
        Type = param_type,
        Overwrite = True,
    )
    print("Putting ", param_name)



results = describe_params() 

for param in results:
    if stage in param['Name']:
        name_value_type = get_params_name_value_type(param) 
        old_param_name = name_value_type[0] 
        new_param_name = change_param_name_suffix(old_param_name) 
        param_value = name_value_type[1]
        param_type = name_value_type[2]
        put_params_in_ps(new_param_name, param_value, param_type, copy_to_region)
    else:
        print(" \n Skipping ", param['Name'], "\n")


