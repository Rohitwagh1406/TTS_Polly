import boto3
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Initialize file serial number
file_serial = 1

def text_to_speech(text):
    global file_serial  # Use global variable for file serial number

    # Initialize AWS Polly client
    polly_client = boto3.client('polly',
                                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                                region_name=os.getenv('AWS_REGION'))

    # Request speech synthesis
    response = polly_client.synthesize_speech(Text=text,
                                               OutputFormat='mp3',
                                               VoiceId='Joanna')

    # Generate unique file name based on current date, time, and file serial number
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = f"{current_datetime}_file{file_serial}.mp3"

    # Save audio data to file
    with open(output_file, 'wb') as f:
        f.write(response['AudioStream'].read())

    # Increment file serial number for the next file
    file_serial += 1

    return output_file

if __name__ == "__main__":
    # Get input text from the user
    text = input("Enter the text you want to convert to speech: ")

    # Convert text to speech and get the file name
    audio_file = text_to_speech(text)

    print("Text to speech conversion complete. Audio file saved as:", audio_file)


# from fastapi import FastAPI
# from pydantic import BaseModel
# import boto3

# app = FastAPI()

# class TextRequest(BaseModel):
#     text: str

# # Initialize AWS S3 client
# s3_client = boto3.client('s3',
#                         aws_access_key_id='YOUR_ACCESS_KEY_ID',
#                         aws_secret_access_key='YOUR_SECRET_ACCESS_KEY',
#                         region_name='YOUR_AWS_REGION')

# def text_to_speech(text, bucket_name, object_key):
#     polly_client = boto3.client('polly',
#                                 aws_access_key_id='YOUR_ACCESS_KEY_ID',
#                                 aws_secret_access_key='YOUR_SECRET_ACCESS_KEY',
#                                 region_name='YOUR_AWS_REGION')

#     response = polly_client.synthesize_speech(Text=text,
#                                                OutputFormat='mp3',
#                                                VoiceId='Joanna')

#     audio_data = response['AudioStream'].read()

#     # Upload audio data to S3 bucket
#     s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=audio_data)

#     # Return the S3 URL of the uploaded audio file
#     s3_url = f"https://{bucket_name}.s3.amazonaws.com/{object_key}"
#     return s3_url

# @app.post("/convert-text-to-speech/")
# async def convert_text_to_speech(request: TextRequest):
#     bucket_name = 'YOUR_S3_BUCKET_NAME'
#     object_key = 'output.mp3'

#     audio_url = text_to_speech(request.text, bucket_name, object_key)
#     return {"audio_url": audio_url}
