import requests
import os

def download_file(url, filename):
    print(f"Downloading sample video to {filename}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print("Download complete!")

if __name__ == "__main__":
    url = "https://github.com/intel-iot-devkit/sample-videos/raw/master/people-detection.mp4"
    if not os.path.exists("sample_video.mp4"):
        download_file(url, "sample_video.mp4")
    else:
        print("sample_video.mp4 already exists!")
