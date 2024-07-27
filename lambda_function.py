import boto3
import json
from decimal import Decimal
from datetime import datetime

print('Loading function')
dynamo = boto3.resource('dynamodb')

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': json.dumps({'error': str(err)}) if err else json.dumps(res, default=str),
        'headers': {
            'Content-Type': 'application/json',
        },
    }
    
def people_in_jasper(items):
    #calculates the number of people still in jasper by Sunday June 7th @5pm
    # The target date and time (June 27, 2024 at 3:00 PM)
    target_datetime = datetime(2024, 6, 27, 15, 0, 0)
    sum = 0
    for item in items:
        longitude = float(item['longitude'])
        latitude = float(item['latitude'])
        date = str(item['timestamp'])
        date = datetime.fromisoformat(date)
        if (longitude > -118.7) and (longitude <-118.5):
            if (latitude > 53.8) and (latitude < 54.0):
                if date > target_datetime:
                    #then this person is in the area of jasper past this time
                    sum += 1
                
    return sum
                
def stuck_in_traffic(items):
    #number of people in jasper alsos stuck in traffic
    sum = 0
    for item in items:
        #if person made "slow traffic" report:
        if str(item['reportType']) == "Slow Area":
            #if person is in Jasper
            longitude = float(item['longitude'])
            latitude = float(item['latitude'])
            date = str(item['timestamp'])
            date = datetime.fromisoformat(date)
            if (longitude > -118.7) and (longitude <-118.5):
                if (latitude > 53.8) and (latitude < 54.0):
                    #if this person's speed is indeeded slow (misinformation prevention)
                    if float(item['currentSpeed_kmh']) < 20.0:
                        sum += 1
                
    return sum
    
    
def lambda_handler(event, context):
    #operation = event['httpMethod']
    operation = "GET"
    
    if operation:
        try:
            table = dynamo.Table("reports-table")
            response = table.scan()
            items = response['Items']
            #perform calculations
            result1 = people_in_jasper(items)
            result2 = stuck_in_traffic(items)
            #return calculated results
            return [result1, result2]
            
        except Exception as e:
            return respond(e)
            
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))