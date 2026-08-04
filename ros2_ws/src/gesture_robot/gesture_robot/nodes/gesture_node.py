"""손 제스처 인식 ROS2 노드."""

import mediapipe as mp
import numpy as np
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
        # object_tracking_node도 같은 토픽에 공 바운딩 박스를 그려 발행하므로
        # (각자 독립적으로 annotate), main_ui는 두 노드 중 먼저 도착한 프레임을
        # 그대로 표시한다.
        self._annotated_publisher = self.create_publisher(
            Image, "camera/image_annotated", best_effort_qos
        )
        self._subscriber = self.create_subscription(
            Image, "camera/image_raw", self._image_callback, best_effort_qos
        )

    def _image_callback(self, msg: Image) -> None:
        frame = self._bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        landmarks = self._detector.detect(frame)
        if not isinstance(landmarks, GestureResult):
            mp.solutions.drawing_utils.draw_landmarks(
                frame, landmarks, mp.solutions.hands.HAND_CONNECTIONS
            )
        result = self._classifier.classify(landmarks)
        self.publish_gesture_command(result, msg.header)
        self._publish_annotated_frame(frame, msg.header)

    def _publish_annotated_frame(self, frame, header) -> None:
        # mediapipe drawing_utils가 배열을 non-contiguous하게 만들 때가 있어
        # cv_bridge 변환 전에 정규화한다.
        frame = np.ascontiguousarray(frame, dtype=np.uint8)
        annotated_msg = self._bridge.cv2_to_imgmsg(frame, encoding="bgr8")
        annotated_msg.header = header
        self._annotated_publisher.publish(annotated_msg)

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
