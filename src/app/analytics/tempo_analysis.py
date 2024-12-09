import numpy as np
from collections import deque
import time

class TempoAnalyzer:
    def __init__(self):
        self.previous_angles = deque(maxlen=5)
        self.previous_times = deque(maxlen=5)
        self.speeds = []

    def analyze_tempo(self, angle):
        """
        Analyze the tempo based on angle changes.

        Args:
            angle (float): Current joint angle.

        Returns:
            dict: Tempo analysis results.
        """
        current_time = time.time()
        self.previous_angles.append(angle)
        self.previous_times.append(current_time)

        if len(self.previous_angles) >= 2:
            angle_difference = abs(self.previous_angles[-1] - self.previous_angles[-2])
            time_difference = self.previous_times[-1] - self.previous_times[-2]
            if time_difference > 0:
                speed = angle_difference / time_difference
                self.speeds.append(speed)
                average_speed = np.mean(self.speeds)
            else:
                speed = 0
                average_speed = 0
        else:
            speed = 0
            average_speed = 0

        return {'current_speed': speed, 'average_speed': average_speed}

    def reset(self):
        self.previous_angles.clear()
        self.previous_times.clear()
        self.speeds.clear()