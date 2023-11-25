import boto3

def send_sns_message(message, message_attributes):
    # Create an SNS client

    sns = boto3.client('sns',
                       region_name='us-east-1',
                       aws_access_key_id="ASIAZCJCIC74YPLGCXHN",
                       aws_secret_access_key="B8TkoU7/fSKz7RKLOA0rdL67//7CAalA/POuVgB1",
                       aws_session_token="FwoGZXIvYXdzEDIaDPmWNk0DofL0nl0KwCLEAencCKRe9fJY/2/+qt6VXRmrkA4sx7VU5UtqqfVL2u9rTaUEl0fgK3lqc2UMxmgZxtiG5UbqjcUYGL1YujAO1ZjVFUwvV0hkjZNOtr+Uf73JCie5r+ZFJ2DuVtLA3Sxu4AEMkI/rxoNv1EroD6huiDOuPPyvwhydAtmc1QZEuYaVEPLAdbUdmKLKnX3sQ2TyJ77J3TxOK9StWERiRmj/Fpu2XuWjClur7a1DV9/IOBYrUwhLWfsWyOW+CqXaK7+SvA1RWywon8KIqwYyLXZTvWjSBf9mCcT7PoI7AAxyN0bl0KsgmKQOaJsagqumbphLxPe9td824/onWA=="
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
