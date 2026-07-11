"""객체 추적 ROS2 노드 골격."""

from typing import Any


class ObjectTrackingNode:
    """카메라 입력과 객체 추적 결과 발행을 담당한다."""

    def __init__(self, camera: Any, tracker: Any, visualizer: Any) -> None:
        # TODO: rclpy Node 상속, 의존 객체 저장, Publisher와 Timer 생성을 구현한다.
        pass

    def process_frame(self) -> None:
        """카메라 프레임 하나를 추적하고 결과를 발행한다."""
        # TODO: 카메라 입력, 객체 추적, 시각화, 결과 발행 순서로 구현한다.
        pass

    def publish_tracking_result(self, tracking_result: Any) -> None:
        """추적 결과를 rosidl 메시지로 발행한다."""
        # TODO: TrackedObject 메시지 변환과 Publisher 발행을 구현한다.
        pass
