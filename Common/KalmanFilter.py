import numpy as np

class KalmanFilter:
    def __init__(self, process_variance: float, measurement_variance: float):
        self.state_estimate = np.zeros(2)  # [x, y] coordinates
        self.covariance_estimate = np.eye(2)  # State covariance matrix
        self.process_variance = process_variance * np.eye(2)  # Process noise
        self.measurement_variance = measurement_variance * np.eye(2)  # Measurement noise

    def predict(self):
        self.covariance_estimate = self.covariance_estimate + self.process_variance

    def update(self, measurement: np.ndarray):
        kalman_gain = self.covariance_estimate @ np.linalg.inv(self.covariance_estimate + self.measurement_variance)
        self.state_estimate = self.state_estimate + kalman_gain @ (measurement - self.state_estimate)
        self.covariance_estimate = (np.eye(2) - kalman_gain) @ self.covariance_estimate

    def get_estimate(self):
        return self.state_estimate