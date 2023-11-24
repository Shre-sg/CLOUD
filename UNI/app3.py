from flask import Flask, render_template, request, session
import os
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload file path flask
UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'This is your secret key to utilize session in Flask'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def mask_data(value):
    # Your masking logic here
    return '***MASKED***'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('index.html', error='No file part')

        file = request.files['file']

        # check if the file is empty
        if file.filename == '':
            return render_template('index.html', error='No selected file')

        # check if the file has the allowed extension
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            return render_template('index2.html')
        else:
            return render_template('index.html', error='Invalid file extension. Allowed extensions are: csv')

    return render_template('index.html')

@app.route('/show_data')
def show_data():
    # Uploaded File Path
    data_file_path = session.get('uploaded_data_file_path', None)

    if data_file_path is None:
        return "No file uploaded. Please upload a file first."

    # Read CSV
    uploaded_df = pd.read_csv(data_file_path, encoding='unicode_escape')

    # Convert to HTML Table without masking
    uploaded_df_html = uploaded_df.to_html(index=False)

    return render_template('show_csv_data.html', data_var=uploaded_df_html)

if __name__ == '__main__':
    app.run(debug=True)
