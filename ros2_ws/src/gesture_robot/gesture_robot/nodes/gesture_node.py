"""손 제스처 인식 ROS2 노드 골격."""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy

from gesture_robot_interfaces.msg import GestureCommand as GestureCommandMsg
from std_msgs.msg import Header

from gesture_robot.core.models import GestureCommand, GestureResult
from gesture_robot.adapters.mediapipe_detector import MediaPipeDetector
from gesture_robot.core.gesture_classifier import GestureClassifier

class GestureNode(Node):
    """손 랜드마크를 제스처 명령으로 변환해 발행한다."""
    def __init__(self, frame_source, detector, classifier):
        # TODO: rclpy Node 상속, 의존 객체 저장, Publisher와 Timer 생성을 구현한다.
        super().__init__("gesture_node")
        self._frame_source = frame_source
        self._detector = detector
        self._classifier = classifier

        qos = QoSProfile(
            depth=10,
            reliability= ReliabilityPolicy.RELIABLE,
        )
        self._publisher = self.create_publisher(
            GestureCommandMsg, "gesture_command", qos
        )
        self._timer = self.create_timer(0.1, self.process_frame)

    def process_frame(self):
        """카메라 프레임 하나에서 제스처를 인식한다."""
        # TODO: 프레임 입력, 손 검출, 제스처 분류, 명령 발행 순서로 구현한다.
        frame = self._frame_source.read()
        if frame is None:
            return
        landmarks = self._detector.detect(frame)
        result = self._classifier.classify(landmarks)
        self.publish_gesture_command(result)

    def publish_gesture_command(self, result):
        """제스처 명령을 rosidl 메시지로 발행한다."""
        # TODO: GestureCommand 메시지 변환과 Publisher 발행을 구현한다.
        msg = GestureCommandMsg()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.command = result.command.value
        msg.confidence = result.confidence
        self._publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)                       # 1. ROS2 켜기
    
    # 의존성 생성
    detector = MediaPipeDetector()              # MediaPipe 검출기
    classifier = GestureClassifier()            # 제스처 분류기
    # TODO: frame_source(카메라)가 준비되면 연결
    # camera = OpenCVCamera()
    # node = GestureNode(frame_source=camera, ...)
    node = GestureNode(frame_source=None,
                       detector=detector,
                        classifier=classifier)  # 2. 노드 생성
    rclpy.spin(node)                            # 3. 계속 실행
    node.destroy_node()                         # 4. ROS2 끄기
    rclpy.shutdown()

if __name__=="__main__":
    main()
