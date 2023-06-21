import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')

    # Print all table names
    try:
        tables = [table.name for table in dynamodb.tables.all()]
        print("Tables in DynamoDB: ", tables)
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'GET,OPTIONS,POST',
                'Access-Control-Allow-Credentials': 'true'
            },
            'body': json.dumps({'message': 'Server error'})
        }

    table = dynamodb.Table('coupons')
    coupon_code = json.loads(event['body'])['coupon']
    
    try:
        response = table.get_item(Key={'coupon_code': coupon_code})
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'GET,OPTIONS,POST',
                'Access-Control-Allow-Credentials': 'true'
            },
            'body': json.dumps({'message': 'Server error'})
        }
    else:
        print("Fetched data from the database: ", response) 
        if 'Item' in response:
            print("Coupon found in the database.") 
            if not response['Item'].get('redeemed'):
                table.update_item(
                    Key={'coupon_code': coupon_code},
                    UpdateExpression='SET redeemed = :val',
                    ExpressionAttributeValues={':val': True}
                )
                return {
                    'statusCode': 200,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                        'Access-Control-Allow-Methods': 'GET,OPTIONS,POST',
                        'Access-Control-Allow-Credentials': 'true'
                    },
                    'body': json.dumps({'message': 'Your link: https://www.udemy.com/course/arduino-zero-to-hero/?couponCode=E18BB491C31CD250164E'})
                }
            else:
                return {
                    'statusCode': 200,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                        'Access-Control-Allow-Methods': 'GET,OPTIONS,POST',
                        'Access-Control-Allow-Credentials': 'true'
                    },
                    'body': json.dumps({'message': 'Coupon already redeemed.'})
                }
        else:
            print("No coupon found in the database.") 
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                    'Access-Control-Allow-Methods': 'GET,OPTIONS,POST',
                    'Access-Control-Allow-Credentials': 'true'
                },
                'body': json.dumps({'message': 'Coupon not found'})
            }
