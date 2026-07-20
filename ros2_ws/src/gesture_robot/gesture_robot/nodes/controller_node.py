"""추적 상태와 로봇 이동 제어 ROS2 노드."""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from geometry_msgs.msg import Twist
from gesture_robot_interfaces.msg import GestureCommand, TrackedObject
from gesture_robot.core.tracking_controller import TrackingController
from gesture_robot.core.tracking_state import TrackingStateMachine


class ControllerNode(Node):
    """제스처와 객체 추적 결과를 이동 명령으로 변환한다."""

    def __init__(self) -> None:
        super().__init__("controller_node")

        self._state_machine = TrackingStateMachine()
        self._controller = TrackingController()

        self._setup_qos()
        self._setup_subscribers()
        self._setup_publisher()

        self.get_logger().info("controller_node 시작됨")

    # 통신 품질 설정
    def _setup_qos(self) -> None:   
        """QoS 프로필을 설정한다."""
        # RELIABLE: 데이터가 중간에 유실되지 않고 반드시 도착하도록 보장
        self._reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )
        # BEST_EFFORT: 데이터 유실을 감수하더라도 가장 최신 데이터를 빨리 보냄
        self._best_effort_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )

    # 제스쳐 인식하는 구독자와 공 객체 탐지 구독자 생성
    def _setup_subscribers(self) -> None:
        """Subscriber를 생성한다."""
        self._gesture_sub = self.create_subscription(
            GestureCommand,
            "/gesture/command",
            self._on_gesture_command,
            self._reliable_qos,
        )
        self._tracking_sub = self.create_subscription(
            TrackedObject,
            "/tracking/result",
            self._on_tracking_result,
            self._best_effort_qos,
        )

    # 거북이에게 명령 내릴 퍼블리셔
    def _setup_publisher(self) -> None:
        """Publisher를 생성한다."""
        self._velocity_pub = self.create_publisher(
            Twist,
            "/turtle1/cmd_vel",
            self._reliable_qos,
        )

    # 제스쳐가 들어올때마다 상태 업데이트
    def _on_gesture_command(self, msg: GestureCommand) -> None:
        """제스처 명령을 수신할 때 호출된다."""
        self._state_machine.update(msg.command)
        state = self._state_machine.current_state()
        self.get_logger().info(
            f"제스처 수신: command={msg.command}, state={state}"
        )

    # 공 객체 추적 결과가 들어올때마다 상태 업데이트
    def _on_tracking_result(self, msg: TrackedObject) -> None:
        """객체 추적 결과를 수신할 때 호출된다."""
        # 객체 추적이 시작되었는지 확인
        tracking_active = self._state_machine.current_state() == "START"

        # 속도 계산
        vel_cmd = self._controller.calculate(
            tracking_active=tracking_active,
            detected=msg.detected,
            error_x=msg.error_x,
            error_y=msg.error_y,
            area=msg.area,
        )

        self._publish_velocity(vel_cmd.linear_x, vel_cmd.angular_z)

    # 최종적으로 속도 계산하여 명령 전달
    def _publish_velocity(self, linear_x: float, angular_z: float) -> None:
        """속도 명령을 발행한다."""
        msg = Twist()
        msg.linear.x = linear_x
        msg.angular.z = angular_z
        self._velocity_pub.publish(msg)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = ControllerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
