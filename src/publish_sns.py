import boto3

def send_sns_message(message, message_attributes):
    # Create an SNS client

    sns = boto3.client('sns',
                       region_name='us-east-1',
                       )



    # Send the message
    try:
        response = sns.publish(
            TopicArn='arn:aws:sns:us-east-1:623378962425:report_changed',
            Message=message,
            MessageAttributes=message_attributes
        )
        print(f"Message sent with ID: {response['MessageId']}")
        return response
    except Exception as e:
        print(f"An error occured: {e}")
        return None
