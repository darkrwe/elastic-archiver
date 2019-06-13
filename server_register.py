import boto3
import requests
from requests_aws4auth import AWS4Auth

service = 'es'
credentials = boto3.Session().get_credentials()


def registerServer(host, region, repository_name, bucket, role_arn):
    try:
        awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service,
                           session_token=credentials.token)
        path = '/_snapshot/' + repository_name
        payload = {
            "type": "s3",
            "settings": {
                "bucket": bucket,
                "region": region,
                "role_arn": role_arn
            }
        }
        headers = {"Content-Type": "application/json"}
        r = requests.put(host + path, auth=awsauth, json=payload, headers=headers)
        if r.status_code is 200:
            return True
        else:
            return False
    except Exception:
        return False
