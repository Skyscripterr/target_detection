from ultralytics import YOLO

class YOLODetector:
    def __init__(self, model_name="yolov8n.pt"):
        print(f"Loading YOLO model: {model_name}...")
        self.model = YOLO(model_name)
        
    def detect(self, frame):
        results = self.model(frame, verbose=False)
        
        detections = []
        result = results[0]
        
        for box in result.boxes:
            x, y, w, h = box.xywh[0].tolist()
            
            confidence = box.conf[0].item()
            class_id = int(box.cls[0].item())
            class_name = self.model.names[class_id]
            
            if confidence > 0.4:
                detections.append({
                    'bbox': [x, y, w, h],
                    'class_name': class_name,
                    'confidence': confidence
                })
                
        return detections
