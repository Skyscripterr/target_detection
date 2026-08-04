import numpy as np

def hungarian_assignment(cost_matrix):
    cost_matrix = np.array(cost_matrix)
    matches = []
    num_tracks = cost_matrix.shape[0]
    num_detections = cost_matrix.shape[1]
    assigned_tracks = set()
    assigned_detections = set()
    
    while len(assigned_tracks) < num_tracks and len(assigned_detections) < num_detections:
        masked_matrix = np.copy(cost_matrix)
        for t in assigned_tracks:
            masked_matrix[t, :] = np.inf
        for d in assigned_detections:
            masked_matrix[:, d] = np.inf
        if np.isinf(masked_matrix).all():
            break

        min_idx = np.unravel_index(np.argmin(masked_matrix), masked_matrix.shape)
        track_idx, det_idx = min_idx[0], min_idx[1]

        matches.append((track_idx, det_idx))
        
        assigned_tracks.add(track_idx)
        assigned_detections.add(det_idx)
        
    unmatched_tracks = [t for t in range(num_tracks) if t not in assigned_tracks]
    unmatched_detections = [d for d in range(num_detections) if d not in assigned_detections]
    
    return np.array(matches), np.array(unmatched_tracks), np.array(unmatched_detections)
