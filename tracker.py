from kalman_filter import KalmanFilter
from hungarian import hungarian_assignment
import numpy as np

def calculate_iou(box1, box2):

    b1_x1, b1_y1 = box1[0] - box1[2]/2, box1[1] - box1[3]/2
    b1_x2, b1_y2 = box1[0] + box1[2]/2, box1[1] + box1[3]/2
    
    b2_x1, b2_y1 = box2[0] - box2[2]/2, box2[1] - box2[3]/2
    b2_x2, b2_y2 = box2[0] + box2[2]/2, box2[1] + box2[3]/2
    
    # Intersection rectangle
    x1 = max(b1_x1, b2_x1)
    y1 = max(b1_y1, b2_y1)
    x2 = min(b1_x2, b2_x2)
    y2 = min(b1_y2, b2_y2)
    
    intersection = max(0, x2 - x1) * max(0, y2 - y1)
    
    area1 = box1[2] * box1[3]
    area2 = box2[2] * box2[3]
    
    union = area1 + area2 - intersection
    if union == 0:
        return 0
    return intersection / union

class Track:
    def __init__(self, bbox, track_id, class_name):
        self.id = track_id
        self.kf = KalmanFilter(bbox)
        self.time_since_update = 0
        self.hits = 1 
        self.class_name = class_name
        
    def predict(self):
        predicted_bbox = self.kf.predict()
        self.time_since_update += 1
        return predicted_bbox
        
    def update(self, bbox):
        self.kf.update(bbox)
        self.time_since_update = 0
        self.hits += 1

class Tracker:
    def __init__(self, max_lost=5):
        self.tracks = []
        self.next_id = 1
        self.max_lost = max_lost
        
    def update(self, detections):
        predicted_boxes = []
        for track in self.tracks:
            predicted_boxes.append(track.predict())
            
        if len(detections) == 0:
            self._cleanup_tracks()
            return self.tracks

        cost_matrix = np.zeros((len(self.tracks), len(detections)))
        for t, predicted_box in enumerate(predicted_boxes):
            for d, detection in enumerate(detections):
                iou = calculate_iou(predicted_box, detection['bbox'])
                cost_matrix[t, d] = 1.0 - iou
                
        matches, unmatched_tracks, unmatched_detections = hungarian_assignment(cost_matrix)
        
        for t, d in matches:
            if cost_matrix[t, d] < 0.7:
                self.tracks[t].update(detections[d]['bbox'])
            else:
                unmatched_tracks = np.append(unmatched_tracks, t)
                unmatched_detections = np.append(unmatched_detections, d)
                
        for d in unmatched_detections:
            new_track = Track(detections[d]['bbox'], self.next_id, detections[d]['class_name'])
            self.tracks.append(new_track)
            self.next_id += 1
            
        self._cleanup_tracks()
        active_tracks = [t for t in self.tracks if t.time_since_update < 1 and t.hits >= 1]
        return active_tracks
        
    def _cleanup_tracks(self):
        self.tracks = [t for t in self.tracks if t.time_since_update <= self.max_lost]
