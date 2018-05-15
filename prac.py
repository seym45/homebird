import boto3
import datetime
import json
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('hbdb')
timestamp = str(datetime.datetime.now())
response = table.scan()

print(json.dumps(response['Items']))

