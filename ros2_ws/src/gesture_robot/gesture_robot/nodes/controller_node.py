"""추적 상태와 이동 제어의 호출 순서를 정의하는 rclpy 노드 골격."""

from typing import Any


class ControllerNode:
    """수신한 명령과 객체 위치를 로봇 속도 명령으로 변환한다."""

    def __init__(self, state_machine: Any, controller: Any) -> None:
        self.state_machine = state_machine
        self.controller = controller

        # TODO: rosidl 메시지 Subscriber와 속도 명령 Publisher를 생성한다.
        self.publisher = None

    def handle_gesture_command(self, gesture_command: Any) -> None:
        """제스처 명령에 따라 추적 상태를 변경한다."""
        self.state_machine.update(gesture_command)

    def handle_tracking_result(self, tracking_result: Any) -> None:
        """현재 상태와 객체 위치를 이용해 이동 명령을 만든다."""
        tracking_state = self.state_machine.current_state()
        velocity_command = self.controller.calculate(
            tracking_state,
            tracking_result,
        )
        self.publish_velocity_command(velocity_command)

    def publish_velocity_command(self, velocity_command: Any) -> None:
        """이동 명령을 ROS2 메시지로 발행한다."""
        # TODO: 속도 메시지 타입을 확정한 뒤 rclpy Publisher로 발행한다.
        raise NotImplementedError
