import os
from contextlib import closing
import boto3
from botocore.exceptions import ClientError 

def list_voices():
    """List all available voices in Amazon Polly."""
    polly = boto3.client('polly')
    try:
        response = polly.describe_voices()
        return response['Voices']
    except ClientError as e:
        print(f"Error fetching voices: {e}")
        return []

def text_to_speech(text, voice_id="Joanna", output_file="outputs/test.mp3"):
    """Convert text to speech using Amazon Polly and save to file."""
    polly = boto3.client('polly')
    try:
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=voice_id
        )
        with closing(response['AudioStream']) as stream:
            with open(output_file, 'wb') as file:
                file.write(stream.read())
        print(f"Audio saved to {output_file}")
    except ClientError as e:
        print(f"Error synthesizing speech: {e}")

input_text = "こんにちは、これはAmazon Pollyのテストです。"
voice_id = "Mizuki"  # Giọng nữ tiếng Nhật

# Convert text to speech and save as output.mp3
text_to_speech(input_text, voice_id)