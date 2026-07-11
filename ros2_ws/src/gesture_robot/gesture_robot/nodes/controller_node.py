"""추적 상태와 로봇 이동 제어 ROS2 노드 골격."""

from typing import Any


class ControllerNode:
    """제스처와 객체 추적 결과를 이동 명령으로 변환한다."""

    def __init__(self, state_machine: Any, controller: Any) -> None:
        # TODO: rclpy Node 상속, Subscriber와 속도 Publisher 생성을 구현한다.
        pass

    def handle_gesture_command(self, gesture_command: Any) -> None:
        """제스처 명령을 소비한다."""
        # TODO: GestureCommand 수신 결과를 추적 상태에 반영한다.
        pass

    def handle_tracking_result(self, tracking_result: Any) -> None:
        """객체 추적 결과를 소비한다."""
        # TODO: TrackedObject와 현재 상태를 이용해 이동 명령을 계산한다.
        pass

    def publish_velocity_command(self, velocity_command: Any) -> None:
        """이동 명령을 ROS2 메시지로 발행한다."""
        # TODO: 속도 메시지 타입 확정 후 Publisher 발행을 구현한다.
        pass
