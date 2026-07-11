"""객체 추적 기능의 호출 순서를 정의하는 rclpy 노드 골격."""

from typing import Any


class ObjectTrackingNode:
    """카메라 입력, 색상 추적, 시각화를 순서대로 조율한다."""

    def __init__(self, camera: Any, tracker: Any, visualizer: Any) -> None:
        self.camera = camera
        self.tracker = tracker
        self.visualizer = visualizer

        # TODO: rclpy Node를 상속하고 TrackedObject Publisher를 생성한다.
        self.publisher = None

    def process_frame(self) -> None:
        """한 프레임의 객체 추적 흐름을 실행한다."""
        frame = self.camera.read()
        tracking_result = self.tracker.track(frame)
        self.visualizer.render(frame, tracking_result)
        self.publish_tracking_result(tracking_result)

    def publish_tracking_result(self, tracking_result: Any) -> None:
        """추적 결과를 rosidl 메시지로 발행한다."""
        # TODO: gesture_robot_interfaces/TrackedObject로 변환하여 발행한다.
        raise NotImplementedError
