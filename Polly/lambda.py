import boto3
import base64
import json
import time

# Initialize AWS clients
polly_client = boto3.client('polly')
s3_client = boto3.client('s3')

# S3 bucket name
S3_BUCKET = "<Your-Bucket-Name>"  # Your input bucket

def lambda_handler(event, context):
    # Get the text to convert from the event
    text = event.get('text', 'Hello, welcome to the demo narration.')
    
    # Define Polly parameters
    voice_id = 'Jasmine'  # Choose a voice
    output_format = 'mp3'  # Output format
    engine_type = 'neural'
    
    try:
        # Call Polly to generate speech
        response = polly_client.synthesize_speech(
            Text=text,
            VoiceId=voice_id,
            OutputFormat=output_format,
            Engine=engine_type
        )
        
        # Read the audio stream
        audio_stream = response['AudioStream'].read()
        
        # Generate a unique filename
        filename = f"narration_{int(time.time())}.mp3"
        
        # Upload the file to S3
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=filename,
            Body=audio_stream,
            ContentType="audio/mpeg"
        )
        
        # Generate the S3 URL
        s3_url = f"s3://{S3_BUCKET}/{filename}"

        return {
            'statusCode': 200,
            'body': {
                'message': 'Success',
                's3_audio_url': s3_url
            }
        }
    
    except Exception as e:
        print(f"Error generating speech: {e}")
        return {
            'statusCode': 500,
            'body': {
                'message': 'Failed to generate audio',
                'error': str(e)
            }
        }
