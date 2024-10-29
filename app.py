from flask import Flask, render_template, jsonify, request
import boto3
import os
from datetime import datetime

app = Flask(__name__)

# S3 Client configuration
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('REACT_APP_AWS_REGION')
)

BUCKET_NAME = os.getenv('REACT_APP_AWS_BUCKET_NAME')

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to fetch recent videos from S3
@app.route('/api/videos')
def get_videos():
    # Fetching list of video files from S3
    videos = fetch_videos_from_s3()
    return jsonify(videos)

def fetch_videos_from_s3():
    # Example function to list files from S3 (use the appropriate folder and filter if needed)
    objects = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix='VIDEO/')
    videos = []

    if 'Contents' in objects:
        for obj in objects['Contents']:
            # Extracting metadata and details of each video
            key = obj['Key']
            videos.append({
                'url': f'https://{BUCKET_NAME}.s3.amazonaws.com/{key}',
                'thumbnail': f'https://{BUCKET_NAME}.s3.amazonaws.com/IMAGE/{os.path.splitext(key)[0]}.jpg',
                'metadata': f'https://{BUCKET_NAME}.s3.amazonaws.com/METADATA/{os.path.splitext(key)[0]}.csv',
                'subtitle': f'https://{BUCKET_NAME}.s3.amazonaws.com/SUBTITLE/{os.path.splitext(key)[0]}-EN.vtt',
            })

    return videos

if __name__ == '__main__':
    app.run(debug=True)
