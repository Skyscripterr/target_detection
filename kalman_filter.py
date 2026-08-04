import numpy as np

class KalmanFilter:
    def __init__(self, bbox):

        x, y, w, h = bbox
        self.state = np.array([x, y, w, h, 0, 0, 0, 0], dtype=float).reshape(-1, 1)

        self.F = np.eye(8)
        for i in range(4):
            self.F[i, i + 4] = 1.0
            
        self.H = np.eye(4, 8)
        
        self.P = np.eye(8) * 10
        for i in range(4, 8):
            self.P[i, i] = 1000

        self.Q = np.eye(8) * 0.01
        self.R = np.eye(4) * 0.1
        
    def predict(self):
        self.state = np.dot(self.F, self.state)
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q
        return self.state[:4].flatten()
        
    def update(self, bbox):
        z = np.array(bbox, dtype=float).reshape(-1, 1)
        y = z - np.dot(self.H, self.state)
        S = np.dot(np.dot(self.H, self.P), self.H.T) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))
        
        self.state = self.state + np.dot(K, y)
        
        I = np.eye(self.P.shape[0])
        self.P = np.dot((I - np.dot(K, self.H)), self.P)
