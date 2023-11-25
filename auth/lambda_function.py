import jwt
import os


def create_policy_document(principalId, effect, resource):
    return {
        "principalId": principalId,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {"Action": "execute-api:Invoke", "Effect": effect, "Resource": resource}
            ],
        },
    }


def lambda_handler(event, context):
    try:
        authHeader = event["headers"]["authorization"]
        if authHeader.startswith("Bearer "):
            token = authHeader[7:]
        else:
            token = "invalid"

        # TODO: The secret is stored as an environment variable but should probably be using a secrets manager
        secret = os.environ.get("JWT_SECRET", "")

        decoded = jwt.decode(token, secret, ["HS256"])
        print(decoded)
        return create_policy_document(decoded["sub"], "Allow", event["routeArn"])

    except Exception as e:
        print(e)
        return create_policy_document("user", "Deny", event["routeArn"])
