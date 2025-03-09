# AWS Polly Text-to-Speech Solution for Demo Videos

This project demonstrates how to build a text-to-speech solution using AWS Polly and AWS Elemental MediaConvert to automatically generate narrated demo videos.

## Architecture Overview

The solution involves the following AWS services:

- **AWS Lambda**: The Lambda function generates speech using AWS Polly and stores the audio file in an S3 bucket.
- **Amazon Polly**: AWS Polly converts the provided text into speech.
- **Amazon S3**: Used to store the Polly-generated audio files and demo videos.
- **AWS Elemental MediaConvert**: This service merges the demo video and Polly's generated audio into a single video file.

## IAM Permissions

Ensure that the Lambda execution role has the necessary permissions for:

- **AWS Polly**: To generate speech.
- **Amazon S3**: To store and retrieve files.
- **AWS Elemental MediaConvert**: To trigger the MediaConvert job for merging audio and video.




