import boto3
import os
from botocore.config import Config
import sys

# This script copies CloudWatch Logs Insights queries into another region
# The region is to be passed as an argument within the command line - var copy_to_region

access_key_id=os.getenv('AWS_ACCESS_KEY_ID')
secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
# aws_region=os.getenv('AWS_REGION')

copy_to_region = sys.argv[1]
client = boto3.client('logs')


def new_config(aws_region):
    my_config = Config(
        region_name= aws_region,
    )
    return my_config

def put_queries_into_another_region(new_config, queries_defs):
    client = boto3.client('logs', config=new_config)

    response = client.put_query_definition(
        name = queries_defs['name'],
        logGroupNames= queries_defs['logGroupNames'],
        queryString = queries_defs['queryString']
    )
    return response



queries = client.describe_query_definitions(
)
definitions=queries["queryDefinitions"]

for i in definitions:
    res = put_queries_into_another_region(new_config(copy_to_region), i)
    print("\n", res, "\n")














