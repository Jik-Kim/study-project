"""단일 카메라 프레임 발행 ROS2 노드."""

import rclpy
from rclpy.node import Node


class CameraNode(Node):
    """카메라 프레임을 /camera/image_raw 토픽으로 발행한다."""

    def __init__(self) -> None:
        super().__init__("camera_node")
        self.get_logger().info("camera_node 시작됨")


def main(args=None) -> None:
    rclpy.init(args=args)
    node = CameraNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
