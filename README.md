 # UAV Target Detection & MOT System

This is a beginner-friendly, modular computer vision pipeline for target detection and Multi-Object Tracking (MOT), designed specifically for UAVs (Unmanned Aerial Vehicles) and edge devices.

## Features
- **Scalable Architecture**: The system cleanly separates the machine learning inference (`detector.py`) from the tracking logic (`tracker.py`, `kalman_filter.py`). This allows you to easily swap YOLOv8 for lighter models (like MobileNet) or heavier models depending on your compute resources.
- **Deployable to Edge Devices**: By using `yolov8n.pt` (the nano version of YOLOv8), this code is specifically tailored to run on edge compute (like a Raspberry Pi 4, Nvidia Jetson Nano, or onboard UAV companion computers) while maintaining high FPS.
- **Docker-Ready**: A `Dockerfile` is provided so you can instantly containerize the application and deploy it uniformly across any hardware architecture.
- **ID Consistent Tracking**: Combines a linear Kalman Filter for motion prediction and an assignment algorithm (Intersection over Union matching) for robust tracking even when objects temporarily overlap.

## How to Run

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download Sample Data**
   Because testing requires video footage, download a sample tracking video:
   ```bash
   python download_sample.py
   ```

3. **Run the Tracker**
   ```bash
   python main.py
   ```
