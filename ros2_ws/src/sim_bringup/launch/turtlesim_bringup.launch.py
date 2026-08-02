from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        # turtlesim 시뮬레이터 노드
        Node(
            package="turtlesim",
            executable="turtlesim_node",
            name="turtlesim_node",
            output="screen",
        ),
        # 카메라 입력 노드
        Node(
            package="gesture_robot",
            executable="camera_node",
            name="camera_node",
            output="screen",
        ),
        # 제스처 인식 노드
        Node(
            package="gesture_robot",
            executable="gesture_node",
            name="gesture_node",
            output="screen",
        ),
        # 색상 객체 추적 노드
        Node(
            package="gesture_robot",
            executable="object_tracking_node",
            name="object_tracking_node",
            output="screen",
        ),
        # 이동 제어 및 상태 관리 노드
        Node(
            package="gesture_robot",
            executable="controller_node",
            name="controller_node",
            output="screen",
        ),
        # 시각화 UI 노드
        Node(
            package="gesture_robot",
            executable="main_ui",
            name="main_ui",
            output="screen",
        ),
    ])
