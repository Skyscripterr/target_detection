import cv2
from detector import YOLODetector
from tracker import Tracker

def main():
    print("Starting UAV Target Detection & MOT System...")
    
    detector = YOLODetector("yolov8n.pt") 
    tracker = Tracker(max_lost=5) 
    
    video_path = "sample_video.mp4" 
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}.")
        print("Please run 'python download_sample.py' first to get a sample video.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))
    
    print("Processing video... Press 'q' to quit the window.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break 

        detections = detector.detect(frame)

        active_tracks = tracker.update(detections)
 
        for track in active_tracks:
            x, y, w, h = track.kf.state[:4].flatten()
            x1 = int(x - w / 2)
            y1 = int(y - h / 2)
            x2 = int(x + w / 2)
            y2 = int(y + h / 2)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            label = f"{track.class_name} ID: {track.id}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("UAV Tracking System", frame)
        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Processing complete. Video saved to output.mp4")

if __name__ == "__main__":
    main()
