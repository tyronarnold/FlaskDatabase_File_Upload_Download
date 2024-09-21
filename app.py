from io import BytesIO
import os

from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://flask_database_example_user:QH9XiIvRg3IpGcoSk4WHWSkC1nvPBpso@dpg-crn6a0g8fa8c738a6re0-a.oregon-postgres.render.com/flask_database_example"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
#postgresql://flask_database_example_user:QH9XiIvRg3IpGcoSk4WHWSkC1nvPBpso@dpg-crn6a0g8fa8c738a6re0-a.oregon-postgres.render.com/flask_database_example
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']

        upload = Upload(filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()

        return f'Uploaded: {file.filename}'
    return render_template('index.html')

@app.route('/download/<upload_id>')
def download(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload.data), attachment_filename=upload.filename, as_attachment=True)