import boto3

def send_sns_message(message, message_attributes):
    # Create an SNS client

    sns = boto3.client('sns',
                       region_name='us-east-1',
                       aws_access_key_id="ASIAZCJCIC74WP65OBUK",
                       aws_secret_access_key="WYGZhLv2uBqzRQt/MVnjc2VgBgXwspMJBZN3T1Xm",
                       aws_session_token="FwoGZXIvYXdzEDEaDCCyXSmSJjrAMShaiyLEAWZnbubkUblLN7rLtlU8P/7psNBFMK0ZFpQBUblkA2/POrH+pXME97A+Q2u1b4YEZt3KAYIhQ87+vvlHoJQde5IhOudm0ijsgI3TszlWGhHa4mYRr8hlgtByPKqXboFQOvdw4e9eccwJqpVRSCmcI5aahPHW+EjLyv4tUMyAg+UVbU1fMWOIEUwB0wp1CzTf1yi1OOwu2KHQ0TGh7NMof9PerkoG6z8tKA5IY04oDyhsuzcWMAoxw09iTn4+EzurC4ivVSgoj5yIqwYyLeBeJpYrnPVbJzjtxaXpSceiYElLB1UpraEy6kxbYwhvFAJiqjqDqi74OAmduA=="
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
