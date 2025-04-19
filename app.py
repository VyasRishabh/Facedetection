from flask import Flask, request, jsonify
from flask_cors import CORS
from deepface import DeepFace
import base64
import tempfile
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


def save_base64_image(base64_str):
    try:
        # Handle the case with or without the header
        if "," in base64_str:
            header, encoded = base64_str.split(",", 1)
        else:
            encoded = base64_str
            
        decoded = base64.b64decode(encoded)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        temp_file.write(decoded)
        temp_file.close()
        return temp_file.name
    except Exception as e:
        print(f"Error saving base64 image: {e}")
        return None

@app.route('/verify-face', methods=['POST', 'OPTIONS'])
def verify_face():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    img1 = data.get('img1')  # URL or base64
    img2 = data.get('img2')  # base64
    
    if not img1 or not img2:
        return jsonify({"error": "Both images are required"}), 400

    temp_files = []
    try:
        # Process first image
        if img1.startswith("data:image/") or img1.startswith("/9j/"):
            img1_path = save_base64_image(img1)
            if img1_path:
                temp_files.append(img1_path)
        else:
            img1_path = img1  # Assume it's a URL
            
        # Process second image
        if img2.startswith("data:image/") or img2.startswith("/9j/"):
            img2_path = save_base64_image(img2)
            if img2_path:
                temp_files.append(img2_path)
        else:
            img2_path = img2  # Assume it's a URL
        
        # Verify faces
        result = DeepFace.verify(
            img1_path=img1_path, 
            img2_path=img2_path,
            model_name="VGG-Face",  # You can choose different models
            distance_metric="cosine"
        )
        
        return jsonify({"verified": result["verified"], "distance": result["distance"]})
    
    except Exception as e:
        print(f"Verification error: {e}")
        return jsonify({"error": str(e)}), 500
    
    finally:
        # Clean up temporary files
        for file_path in temp_files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error removing temp file {file_path}: {e}")

if __name__ == '__main__':
    app.run(debug=True)
