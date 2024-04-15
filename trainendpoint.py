from flask import Flask, jsonify, request
import threading
import queue
import json
import os
import tempfile
import subprocess
import shutil
from werkzeug.utils import secure_filename

app = Flask(__name__)
task_queue = queue.Queue()

processing = False  # Global flag to indicate processing status
def allowed_file(filename):
    # Replace the following line with your file validation logic
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'wav', 'mp3'}

def update_status(status_file_path, new_status, details):
    try:
        with open(status_file_path, 'r+') as file:
            status = json.load(file)
            status['status'] = new_status
            status['details'] = details
            file.seek(0)
            json.dump(status, file, indent=4)
            file.truncate()
    except Exception as e:
        print(f"Failed to update status: {e}")


def worker():
    while True:
        task = task_queue.get()
        if task is None:
            break  # Allows the thread to end cleanly
        
        model_name, file_paths, status_file_path = task
        tmpdirname = tempfile.mkdtemp(dir=os.getcwd())
        
        try:
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(tmpdirname, filename)
                    file.save(filepath)

            log_dir = os.path.join('logs', model_name)
            os.makedirs(log_dir, exist_ok=True)
            
            for filepath in file_paths

                subprocess.run(['python', 'trainset_preprocess_pipeline_print.py', tmpdirname, '40000', '12', log_dir, 'False'], check=True)
                update_status(status_file_path, 'preprocess', 'Preprocessing done.')

                subprocess.run(['python', 'extract_f0_print.py', log_dir, '12', 'harvest'], check=True)
                subprocess.run(['python', 'extract_feature_print.py', 'cuda:0', '1', '0', '0', log_dir], check=True)
                update_status(status_file_path, 'features', 'Feature extraction done.')

                subprocess.run(['python', 'pretrain.py', '--exp_dir1', model_name, '--sr2', '40k', '--if_f0_3', '1', '--spk_id5', '0'], check=True)
                subprocess.run(['python3', 'train_nsf_sim_cache_sid_load_pretrain.py', '-e', model_name, '-sr', '40k', '-f0', '1', '-bs', '19', '-g', '0', '-te', '200', '-se', '50', '-pg', 'pretrained/f0G40k.pth', '-pd', 'pretrained/f0D40k.pth', '-l', '0', '-c', '0'], check=True)
            update_status(status_file_path, 'completed', 'Processing completed successfully.')

        except Exception as e:
            update_status(status_file_path, 'failed', f'Processing failed: {str(e)}')

        finally:
            shutil.rmtree(tmpdirname)
            task_queue.task_done()

threading.Thread(target=worker, daemon=True).start()

@app.route('/process_audio', methods=['POST'])
def process_audio():
    global processing
    if processing:
        return jsonify({'error': 'Another process is currently running. Please try again later.'}), 429

    status_dir = 'status'
    os.makedirs(status_dir, exist_ok=True)
    status_file_path = os.path.join(status_dir, 'status.json')

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    files = request.files.getlist('file')
    model_name = request.form.get('model_name', '')
    if not model_name:
        return jsonify({'error': 'Model name is required'}), 400

    if not files or all(file.filename == '' for file in files):
        return jsonify({'error': 'No selected files'}), 400

    file_paths = []
    tmpdirname = tempfile.mkdtemp(dir=os.getcwd())
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(tmpdirname, filename)
            file.save(filepath)
            file_paths.append(filepath)

    with open(status_file_path, 'w') as file:
        json.dump({'status': 'queued', 'details': 'Your request is queued for processing.'}, file)

    task_queue.put((model_name, file_paths, status_file_path))
    return jsonify({'success': True, 'message': 'Your request is queued.', 'status_path': status_file_path})


@app.route('/status', methods=['GET'])
def get_status():
    status_file_path = os.path.join('status', 'status.json')
    if os.path.exists(status_file_path):
        with open(status_file_path, 'r') as file:
            status = json.load(file)
        return jsonify(status)
    else:
        return jsonify({'status': 'unknown', 'details': 'Status file not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
