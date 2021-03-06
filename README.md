# elastic-archiver

RESTFUL Python Flask powered AWS ElasticSearch Service index archiver

## Prerqusities

* Create Database using `schema.create.sql`;
* pip install -U Flask
* pip install peewee
* pip install pysqlite (unix/macos)
* in windows you can use sqlite3.exe ~/util


## Create Role Policy File

create `role-policy.json` file as like below using file editor:

 {
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "",
    "Effect": "Allow",
    "Principal": {
      "Service": "es.amazonaws.com"
    },
    "Action": "sts:AssumeRole"
  }]
 }

## Create Aws Iam Role

Execute below command using aws sdk;

$ aws iam create-role --role-name role --assume-role-policy-document file://role-policy.json

Here is example response for creating role:

{
    "Role": {
        "Path": "/",
        "RoleName": "role",
        "RoleId": "A...6",
        "Arn": "arn:aws:iam::$accountId:role/role",
        "CreateDate": "2019-06-13T08:13:04Z",
        "AssumeRolePolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "es.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
    }
}

## Create s3 Bucket

create bucket "data" on your s3.

## Attach Inline Policy to your role

Attach inline below policy to the role "role"

inline policy name: `inline-policy`

   {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "s3:ListBucket"
            ],
            "Effect": "Allow",
            "Resource": [
                "arn:aws:s3:::data"
            ]
        },
        {
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Effect": "Allow",
            "Resource": [
                "arn:aws:s3:::data/*"
            ]
        }
    ]
  }
  
## Add and Register your Aws Es cluster servers


## Authors - Version 1.0
* Emin İnal
