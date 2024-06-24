import os

from flask import Flask, request, render_template, jsonify, url_for
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# AIzaSyBfkd99S201FLBZohkHmsAnSj0ohCx30QI

# from example import uploadVideo

app = Flask(__name__)

# Ensure the upload folder exists
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
	os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/privacy-policy')
def privacy_policy():
	return render_template('privacy_policy.html')


@app.route('/terms-of-service')
def terms_of_service():
	return render_template('terms-of-service.html')


@app.route('/uploads', methods=['POST'])
def upload():
	video = request.files['video']
	description = request.form['description']
	tags = request.form['tags']
	hashtags = request.form['hashtags']
	platforms = request.form.getlist('platforms')
	
	# Save the video file
	video_path = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
	video.save(video_path)
	
	# Handle uploading to selected platforms (placeholders)
	for platform in platforms:
		if platform == 'tiktok':
			upload_to_tiktok(video_path, description, tags, hashtags)
		elif platform == 'instagram':
			upload_to_instagram(video_path, description, tags, hashtags)
		elif platform == 'youtube':
			upload_to_youtube(video_path, description, tags, hashtags)
	
	# Return the video URL for the frontend to display
	video_url = url_for('static', filename=f'uploads/{video.filename}')
	return jsonify({'video_url': video_url})


def upload_to_tiktok(video_path, description, tags, hashtags):
	pass


def upload_to_instagram(video_path, description, tags, hashtags):
	# Implement Instagram API integration here
	pass


def upload_to_youtube(video_path, description, tags, hashtags):
	# Load credentials from the 'client_secrets.json' file
	client_secrets_file = r"C:\Users\Sami\Downloads\client_secret_91682115656-1k42hk9urbgdvur221v08ei1brgn00a8.apps.googleusercontent.com.json"
	
	flow = InstalledAppFlow.from_client_secrets_file(
		client_secrets_file,
		scopes=['https://www.googleapis.com/auth/youtube.upload']
	)
	credentials = flow.run_local_server(port=8080)
	
	# Build the service
	youtube = build('youtube', 'v3', credentials=credentials)
	
	# Define the metadata for the video
	body = {
		'snippet': {
			'title': description,
			'description': description,
			'tags': tags.split(','),
		},
		'status': {
			'privacyStatus': 'unlisted'  # or 'private' or 'public'
		}
	}
	
	# Define the media file
	media = MediaFileUpload(video_path, mimetype='video/*')
	
	# Call the API's videos.insert method to upload the video
	request = youtube.videos().insert(
		part=','.join(body.keys()),
		body=body,
		media_body=media
	)
	response = request.execute()
	
	return response


if __name__ == '__main__':
	app.run(debug=True)
