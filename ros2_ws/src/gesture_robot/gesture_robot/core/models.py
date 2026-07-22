"""노드 내부에서 사용할 Python 데이터 모델 정의 영역."""

from enum import Enum

class GestureCommand(Enum):
    NONE = 0
    START = 1
    STOP = 2

class GestureResult:
    def __init__(self, command: GestureCommand, confidence: float):
        self.command = command
        self.confidence = confidence

class TrackingResult:
    def __init__(self, detected: bool, error_x: float, error_y: float, area: float):
        self.detected = detected
        self.error_x = error_x
        self.error_y = error_y
        self.area = area

class VelocityCommand:
    def __init__(self, linear_x: float, angular_z: float):
        self.linear_x = linear_x
        self.angular_z = angular_z