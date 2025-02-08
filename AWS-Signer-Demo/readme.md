The AWS-Signer-CF-Template.yaml file creates an API Gateway and lambda function for you
- Save the .yaml file to your machine and upload it to cloudformation in AWS Console
- Follow the guide on medium to learn how to create a signing profile and signing job to sign your lambda function
- Delete the stack in cloudformation to delete all the resources and log groups that are created as part of the CF template
- The CF template was tested on us-east-1 region


The sample-container-app has all resources needed to create a sample container app 
- We will use the sample app to push the container to ECR and sign in
