import boto3
import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('hbdb')
timestamp = str(datetime.datetime.now())
table.put_item(
	Item={

		'name':'emma',
		'url':r'http://homebird.s3.amazonaws.com/dataset/id_1/emmastone/9.jpg',
		'timestamp':timestamp,
	}
)


print(table.creation_date_time)

