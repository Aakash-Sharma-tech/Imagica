from flask import Flask, render_template, jsonify, request
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
#from config import api_key, cloud_name, api_secret
import os
from cloudinary import CloudinaryImage

api_key=os.getenv("api_key")
cloud_name=os.getenv("cloud_name")
api_secret=os.getenv("api_secret")
# Load configuration from config.json

app = Flask(__name__)

# Configuration       
cloudinary.config(
    cloud_name=cloud_name,
    api_key=api_key,
    api_secret=api_secret,
    secure=True
)
print(api_key, cloud_name, api_secret)


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/playground')
def playground():
    return render_template('playground.html')

# Upload route
@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        print("FILES:", request.files)  # DEBUG LINE
        file_to_upload = request.files.get('file')
        if file_to_upload:
            print("Uploading:", file_to_upload.filename)
            upload_result = cloudinary.uploader.upload(file_to_upload)
            print("Uploaded to Cloudinary:", upload_result)
            return jsonify({
                'url': upload_result['secure_url'],
                'public_id': upload_result['public_id']
            })
        return jsonify({'error': 'No file uploaded'}), 400
    except Exception as e:
        print("❌ Error during upload:", e)
        return jsonify({'error': 'Upload failed', 'details': str(e)}), 500

# Process image route (testing by showing the same image)
@app.route('/process', methods=['POST'])
def process_image():
    data = request.get_json()
    public_id = data.get('public_id')
    action = data.get('action')
     
    if(action == "remove_bg"):
        img_tag = CloudinaryImage(public_id).image(effect="background_removal")
        start_pos = img_tag.find('src="') + len('src="')

        end_pos = img_tag.find('"', start_pos)

      
        img_url = img_tag[start_pos:end_pos]
        return jsonify({
            'processed_url': img_url
        })

    elif (action == "resize"):
        img_tag = CloudinaryImage(public_id).image(gravity="auto", height=940, width=880, crop="auto")
       
        start_pos = img_tag.find('src="') + len('src="')
        end_pos = img_tag.find('"', start_pos)

        img_url = img_tag[start_pos:end_pos]
        return jsonify({
            'processed_url': img_url
        })
    
    elif(action=='enhance'):
        img_tag = CloudinaryImage(public_id).image(effect="enhance")
        start_pos = img_tag.find('src="') + len('src="')
        end_pos = img_tag.find('"', start_pos)

        img_url = img_tag[start_pos:end_pos]
        return jsonify({
            'processed_url': img_url
        })
    elif(action == "Generative Fill"):
        img_tag = CloudinaryImage("samples/outdoor-woman").image(aspect_ratio="8:5", background="gen_fill", crop="pad")
        start_pos = img_tag.find('src="') + len('src="')
        end_pos = img_tag.find('"', start_pos)

        img_url = img_tag[start_pos:end_pos]
        return jsonify({
            'processed_url': img_url
        })
    elif(action == "Sharp"):
        img_tag = CloudinaryImage("samples/coffee").image(effect="sharpen:150")
        start_pos = img_tag.find('src="') + len('src="')
        end_pos = img_tag.find('"', start_pos)

        img_url = img_tag[start_pos:end_pos]
        return jsonify({
            'processed_url': img_url
        })
        

app.run(debug=True)
