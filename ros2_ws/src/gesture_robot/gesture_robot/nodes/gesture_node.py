"""손 제스처 인식 ROS2 노드."""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from gesture_robot_interfaces.msg import GestureCommand as GestureCommandMsg
from std_msgs.msg import Header

from gesture_robot.core.models import GestureCommand, GestureResult
from gesture_robot.adapters.mediapipe_detector import MediaPipeDetector
from gesture_robot.core.gesture_classifier import GestureClassifier

class GestureNode(Node):
    """손 랜드마크를 제스처 명령으로 변환해 발행한다."""
    def __init__(self):
        super().__init__("gesture_node")

        self.declare_parameter("max_num_hands", 1)
        self.declare_parameter("min_detection_confidence", 0.7)
        self.declare_parameter("min_tracking_confidence", 0.5)

        self._detector = MediaPipeDetector(
            max_num_hands=self.get_parameter("max_num_hands").value,
            min_detection_confidence=self.get_parameter("min_detection_confidence").value,
            min_tracking_confidence=self.get_parameter("min_tracking_confidence").value,
        )
        self._classifier = GestureClassifier()
        self._bridge = CvBridge()

        reliable_qos = QoSProfile(
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
        )
        best_effort_qos = QoSProfile(
            depth=1,
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
        )

        self._publisher = self.create_publisher(
            GestureCommandMsg, "gesture/command", reliable_qos
        )
        self._subscriber = self.create_subscription(
            Image, "camera/image_raw", self._image_callback, best_effort_qos
        )

    def _image_callback(self, msg: Image) -> None:
        frame = self._bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        landmarks = self._detector.detect(frame)
        result = self._classifier.classify(landmarks)
        self.publish_gesture_command(result, msg.header)

    def publish_gesture_command(self, result, header=None):
        msg = GestureCommandMsg()
        if header is not None:
            msg.header = header
        else:
            msg.header = Header()
            msg.header.stamp = self.get_clock().now().to_msg()
        msg.command = result.command.value
        msg.confidence = result.confidence
        self._publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = GestureNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
