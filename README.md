# AWSLabs

Download the AWS-Xray-Lambda-Function.py and paste it into your own lambda function 

Download the packaged file Python and create a Layer in Lambda - This is for Xray SDK 

Create an API Gateway with 2 resources todo and ui (Enable Lambda Proxy Integration) 

Integrate the API gateway with Lambda Function your created earlier 

Associate the necessary permissions to the lambda exection role to enable communication with DynamoDB and perform put operations on Xray
Example permissions listed below:
AmazonDynamoDBFullAccess
AWSXRayDaemonWriteAccess
AWSXrayFullAccess

Create a DynamoDB table and input some test data
DynamoDB Schema
id (String)
status (String)
title (String)

*Note: It is recommended to abide by the permissions of least privilege when assigning permission to IAM Roles, for demo purposes i have used FullAccess.
