import boto3
import os
import time
location = 'us-east-2'
bucket_name = 'homebird'
dynamodb = 'hbdb'
table_status= ''
debug_aws = False
bucket_url = r'http://s3-us-east-2.amazonaws.com/homebird/'



def put_item_bucket(sourcename,targetname):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(sourcename, bucket_name, targetname)
    except:
        print('Error '+ put_item_bucket.__name__)


def put_item_db(tablename, data):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tablename)
    try:
        table.put_item(
            Item=data
        )
    except:
        print('data format error')

def get_item__db(tablename):
    dynamodb = boto3.resource('dynamodb')
    try:
        table = dynamodb.Table(tablename)
        response = table.scan()
    except:
        if debug_aws: print('Table Name Error')
        response = None

    return response['Items']

def comapare_faces(source_bucket_key,target_bucket_key):
    confidence = None
    client = boto3.client('rekognition',location)
    response = client.compare_faces(SimilarityThreshold=70,
                                    SourceImage={'S3Object': {'Bucket': bucket_name, 'Name': source_bucket_key}},
                                    TargetImage={'S3Object': {'Bucket': bucket_name, 'Name': target_bucket_key}})
    for faceMatch in response['FaceMatches']:
        # position = faceMatch['Face']['BoundingBox']
        confidence = faceMatch['Face']['Confidence']
    return confidence


def compare_faces_among_all(unknown_key, known_keys):
    matched_key = None
    max_confidence = 0
    print(compare_faces_among_all.__name__)
    for key in known_keys:
        confidence = comapare_faces(key, unknown_key)
        print(confidence)
        if confidence and confidence > max_confidence:
            matched_key = key
            max_confidence = confidence
    return matched_key


if __name__ == "__main__":
    a = time.time()
    # source_bucket_key='mehedi.jpg'
    # target_bucket_key = 'mehedi.jpg'
    # confidence = comapare_faces(source_bucket_key, target_bucket_key)
    # print(confidence)
    unknown_key ='15264950001823323.jpg'
    keys = ['15264951915330803.jpg', '15263994164066347.jpg']
    print(compare_faces_among_all(unknown_key,keys))
    print('Elapsed time: ' + str(time.time()-a))


# if __name__ == "__main__":
#     b = time.time()
#     print(time.time()-b)
