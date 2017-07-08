import boto3
import datetime

# Upload a temperature reading for a
# particular location and sensor
def putData(location, sensor, temperature):

    client = boto3.client('cloudwatch')

    client.put_metric_data(
        Namespace='weather-station',
        MetricData=[
            {
                'MetricName': 'Temperature',
                'Dimensions': [
                    {
                        'Name': 'Location',
                        'Value': location
                    },
                    { 
                        'Name': 'Sensor',
                        'Value': sensor
                    },
                ],
                'Timestamp': datetime.datetime.utcnow(),
                'Value': temperature,
                'Unit': 'None'
            },
        ]
    )
    return;
