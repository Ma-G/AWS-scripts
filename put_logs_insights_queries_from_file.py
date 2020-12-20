import boto3
import os
from botocore.config import Config
import sys
import json

# This script copies CloudWatch Logs Insights queries from a file into a given region
# The region is to be passed as an argument within the command line - var copy_to_region
# The file is to be passed as a second parameter
# Eg. run: aws logs describe-query-definitions --output json  > [file_name]

access_key_id=os.getenv('AWS_ACCESS_KEY_ID')
secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')


if len(sys.argv) == 3 and os.path.isfile(sys.argv[2]):
    copy_to_region = sys.argv[1]
    queries_file = sys.argv[2]
else:
    print("\n\
    Incorrect arguments.\n Expected: AWS region and path to a json file\n \n")
    exit

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


with open(queries_file) as json_file:
    queries = json.load(json_file)
    definitions=queries["queryDefinitions"]

for i in definitions:
    res = put_queries_into_another_region(new_config(copy_to_region), i)
    print("\n", res, "\n")
