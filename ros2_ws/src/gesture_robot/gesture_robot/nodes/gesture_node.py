"""손 제스처 기능의 호출 순서를 정의하는 rclpy 노드 골격."""

from typing import Any


class GestureNode:
    """손 검출, 제스처 분류, 명령 발행을 순서대로 조율한다."""

    def __init__(self, frame_source: Any, detector: Any, classifier: Any) -> None:
        self.frame_source = frame_source
        self.detector = detector
        self.classifier = classifier

        # TODO: rclpy Node를 상속하고 GestureCommand Publisher를 생성한다.
        self.publisher = None

    def process_frame(self) -> None:
        """한 프레임의 제스처 인식 흐름을 실행한다."""
        frame = self.frame_source.read()
        hand_landmarks = self.detector.detect(frame)
        gesture_command = self.classifier.classify(hand_landmarks)
        self.publish_gesture_command(gesture_command)

    def publish_gesture_command(self, gesture_command: Any) -> None:
        """제스처 명령을 rosidl 메시지로 발행한다."""
        # TODO: gesture_robot_interfaces/GestureCommand로 변환하여 발행한다.
        raise NotImplementedError
