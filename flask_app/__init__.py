from flask import Flask
import os

app = Flask(__name__)
upload_folder = os.path.join(app.root_path, 'static/uploads')

app.secret_key = "shhhhhh"
app.config['UPLOAD_FOLDER'] = upload_folder 