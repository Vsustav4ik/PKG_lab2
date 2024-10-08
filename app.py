from flask import Flask, render_template, request
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_image_info(file_path):
    with Image.open(file_path) as img:
        return {
            "filename": os.path.basename(file_path),
            "size": img.size,
            "dpi": img.info.get('dpi', (None, None)),
            "color_depth": img.mode,
            "compression": img.info.get('compression', 'N/A')
        }

@app.route('/', methods=['GET', 'POST'])
def index():
    images_info = []
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        for file in files:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            try:
                images_info.append(get_image_info(file_path))
            except Exception as e:
                print(f"Error processing {file.filename}: {e}")
    return render_template('index.html', images_info=images_info)

if __name__ == '__main__':
    app.run(debug=True)