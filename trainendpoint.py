from flask import Flask, redirect, url_for, render_template,session,request,jsonify
import subprocess
import os
import uuid 
import json
import tempfile
from werkzeug.utils import secure_filename
import shutil

app = Flask(__name__)

# Allowed extensions for the audio files
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a'}

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def update_status(status_file_path, new_status, details):
    """
    Updates the processing status in a specified JSON file.

    Parameters:
    - status_file_path: str, the path to the JSON status file.
    - new_status: str, the new status to write (e.g., 'completed', 'failed').
    - details: str, a descriptive message about the new status.
    """
    if os.path.exists(status_file_path):
        # Open the existing status file
        with open(status_file_path, 'r+') as file:
            status = json.load(file)
            # Update the status
            status['status'] = new_status
            status['details'] = details
            # Go back to the start of the file to overwrite it
            file.seek(0)
            json.dump(status, file, indent=4)  # Using indent for better readability
            # Truncate the file to the current position
            file.truncate()
    else:
        print(f"Error: The status file {status_file_path} does not exist.")

@app.route('/')
def index():
    # Serve the file upload form
    return render_template('train.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    """Endpoint to upload files and trigger processing."""
    
    status_dir = 'status'
    os.makedirs(status_dir, exist_ok=True)
    status_file_path = os.path.join(status_dir, 'status.json')

    status = {'status': 'initiated', 'details': ''}
    with open(status_file_path, 'w') as file:
        json.dump(status, file)

    
    if 'file' not in request.files:
        status['status'] = 'failed'
        status['details'] = 'No file part'
        return jsonify({'error': 'No file part'}), 400

    files = request.files.getlist('file')
    model_name = request.form.get('model_name', '')
    if not model_name:
        return jsonify({'error': 'Model name is required'}), 400

    if not files or all(file.filename == '' for file in files):
        return jsonify({'error': 'No selected files'}), 400

    # Create a temporary directory for this upload session
    tmpdirname = tempfile.mkdtemp(dir=os.getcwd())
    try:
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(tmpdirname, filename)
                file.save(filepath)

        # After saving all files to the temporary directory, call the scripts
        log_dir = f'logs/{model_name}'
        os.makedirs(log_dir, exist_ok=True)  # Ensure log directory exists

        # Assuming your scripts are modified to accept a directory of audio files
        subprocess.run(['python', 'trainset_preprocess_pipeline_print.py', tmpdirname, '40000', '12', log_dir, 'False'], check=True)
        
        
        new_status = 'preprocess'  # This can be changed as needed
        details = 'pre processing done.'  # Customize the detail message as needed
        update_status(status_file_path, new_status, details)

        
        
        subprocess.run(['python', 'extract_f0_print.py', log_dir, '12', 'harvest'], check=True)
        subprocess.run(['python', 'extract_feature_print.py', 'cuda:0', '1', '0', '0', log_dir], check=True)
        
        new_status = 'features'  # This can be changed as needed
        details = 'feature extraction done.'  # Customize the detail message as needed
        update_status(status_file_path, new_status, details)

        
        subprocess.run(['python', 'pretrain.py', '--exp_dir1', model_name, '--sr2', '40k', '--if_f0_3', '1', '--spk_id5', '0'], check=True)
        subprocess.run(['python3', 'train_nsf_sim_cache_sid_load_pretrain.py', '-e', model_name, '-sr', '40k', '-f0', '1', '-bs', '19', '-g', '0', '-te', '200', '-se', '50', '-pg', 'pretrained/f0G40k.pth', '-pd', 'pretrained/f0D40k.pth', '-l', '0', '-c', '0'], check=True)
        
        status_dir = 'status'
        status_file_path = os.path.join(status_dir, 'status.json')
        new_status = 'completed'  # This can be changed as needed
        details = 'Processing completed successfully.'  # Customize the detail message as needed
        update_status(status_file_path, new_status, details)
        
        return jsonify({'success': True, 'message': 'Files processed successfully.'})
        
        
        
    except Exception as e:

        status_dir = 'status'
        status_file_path = os.path.join(status_dir, 'status.json')
        new_status = 'failed'  # This can be changed as needed
        details = 'Processing failed.'  # Customize the detail message as needed
        update_status(status_file_path, new_status, details)


        model_path = os.path.join('weights', f'{model_name}.pth')
        if os.path.isfile(model_path):
            return jsonify({'success': True, 'message': 'Files processed with errors.', 'details': str(e)})
        else:
            return jsonify({'error': 'An error occurred during processing', 'details': str(e)}), 500
        return jsonify({'error': 'An error occurred during processing', 'details': str(e)}), 500
    finally:
        # Optionally remove the temporary directory after processing if no longer needed
          shutil.rmtree(tmpdirname)

@app.route('/status', methods=['GET'])
def get_status():
    status_dir = 'status'
    status_file_path = os.path.join(status_dir, 'status.json')
    
    if os.path.exists(status_file_path):
        with open(status_file_path, 'r') as file:
            status = json.load(file)
        return jsonify(status)
    else:
        return jsonify({'status': 'unknown', 'details': 'Status file not found'}), 404



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
