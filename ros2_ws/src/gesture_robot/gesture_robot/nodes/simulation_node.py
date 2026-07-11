"""시뮬레이터 연동의 호출 순서를 정의하는 rclpy 노드 골격."""

from typing import Any


class SimulationNode:
    """수신한 이동 명령을 시뮬레이터 어댑터에 전달한다."""

    def __init__(self, simulator: Any) -> None:
        self.simulator = simulator

        # TODO: rclpy Node를 상속하고 이동 명령 Subscriber를 생성한다.

    def handle_velocity_command(self, velocity_command: Any) -> None:
        """이동 명령을 시뮬레이터에 적용한다."""
        self.simulator.apply_velocity(velocity_command)
