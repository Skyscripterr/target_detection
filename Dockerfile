# Use an official lightweight Python image
FROM python:3.9-slim

# Install system dependencies required for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Download the sample video automatically during build
RUN python download_sample.py

# Command to run the application
# Note: If running inside Docker without a GUI, cv2.imshow will fail. 
# main.py is already setup to write to 'output.mp4'.
CMD ["python", "main.py"]
