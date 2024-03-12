# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    ffmpeg \
    aria2 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone the specific GitHub repository and checkout the stable branch
RUN git clone https://github.com/allthingssecurity/rvc.git \
    && cd rvc \
    && git checkout stable

# Set the working directory to the cloned repository
WORKDIR /usr/src/app/rvc

# Copy the requirements.txt file into the container
COPY requirements.txt ./

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install additional Python packages
RUN pip install --no-cache-dir faiss-cpu==1.7.2 fairseq gradio==3.14.0 ffmpeg-python praat-parselmouth pyworld numpy==1.23.5 numba==0.56.4 librosa==0.9.2 flask av boto3

RUN pip install --no-cache-dir cloudinary

# Create directories for pretrained models and weights
RUN mkdir -p pretrained uvr5_weights

# Download pretrained models and UVR5 weights
# You can chain multiple aria2c commands together using "&& \"
RUN aria2c --console-log-level=error -c -x 16 -s 16 -k 1M -d pretrained -o D32k.pth https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/pretrained/D32k.pth && \
    aria2c --console-log-level=error -c -x 16 -s 16 -k 1M -d pretrained -o D40k.pth https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/pretrained/D40k.pth && \
	aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/pretrained/D48k.pth -d pretrained -o D48k.pth && \
    aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/pretrained/G32k.pth -d pretrained -o G32k.pth && \
    aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/pretrained/G40k.pth -d pretrained -o G40k.pth && \
    aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/pretrained/G48k.pth -d pretrained -o G48k.pth && \

    aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/pretrained/f0D32k.pth -d pretrained -o f0D32k.pth && \
    aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/pretrained/f0D40k.pth -d pretrained -o f0D40k.pth && \
    aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/pretrained/f0D48k.pth -d pretrained -o f0D48k.pth && \
    aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/pretrained/f0G32k.pth -d pretrained -o f0G32k.pth && \
    aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/pretrained/f0G40k.pth -d pretrained -o f0G40k.pth && \
    aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/pretrained/f0G48k.pth -d pretrained -o f0G48k.pth && \

    # Add additional aria2c commands for each model and weight file
    aria2c --console-log-level=error -c -x 16 -s 16 -k 1M -d uvr5_weights -o HP2-人声vocals+非人声instrumentals.pth https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/uvr5_weights/HP2-人声vocals+非人声instrumentals.pth && \
    aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/uvr5_weights/HP5-主旋律人声vocals+其他instrumentals.pth -d uvr5_weights -o HP5-主旋律人声vocals+其他instrumentals.pth && \

# Download additional models
    aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/hubert_base.pt  -o hubert_base.pt && \
    aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/rmvpe.pt  -o rmvpe.pt 
	

# Set the environment variable for Flask
ENV FLASK_APP=trainendpoint.py

# Expose the port Flask is running on
EXPOSE 5000

# Command to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
