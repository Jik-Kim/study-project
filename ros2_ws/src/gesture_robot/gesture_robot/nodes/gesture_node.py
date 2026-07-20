"""손 제스처 인식 ROS2 노드 골격."""

from typing import Any


class GestureNode:
    """손 랜드마크를 제스처 명령으로 변환해 발행한다."""

    def __init__(self, frame_source: Any, detector: Any, classifier: Any) -> None:
        # TODO: rclpy Node 상속, 의존 객체 저장, Publisher와 Timer 생성을 구현한다.
        pass

    def process_frame(self) -> None:
        """카메라 프레임 하나에서 제스처를 인식한다."""
        # TODO: 프레임 입력, 손 검출, 제스처 분류, 명령 발행 순서로 구현한다.
        pass

    def publish_gesture_command(self, gesture_command: Any) -> None:
        """제스처 명령을 rosidl 메시지로 발행한다."""
        # TODO: GestureCommand 메시지 변환과 Publisher 발행을 구현한다.
        pass
