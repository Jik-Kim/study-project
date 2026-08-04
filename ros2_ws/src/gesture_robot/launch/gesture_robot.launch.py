"""전체 시스템 통합 실행 구성을 관리하는 Launch 파일."""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    """팀에서 구현한 노드들과 파라미터(params.yaml)를 등록한다."""
    pkg_dir = get_package_share_directory("gesture_robot")
    param_file = os.path.join(pkg_dir, "config", "params.yaml")

    camera_node = Node(
        package="gesture_robot",
        executable="camera_node",
        name="camera_node",
        parameters=[param_file],
        output="screen",
    )

    gesture_node = Node(
        package="gesture_robot",
        executable="gesture_node",
        name="gesture_node",
        parameters=[param_file],
        output="screen",
    )

    object_tracking_node = Node(
        package="gesture_robot",
        executable="object_tracking_node",
        name="object_tracking_node",
        parameters=[param_file],
        output="screen",
    )

    controller_node = Node(
        package="gesture_robot",
        executable="controller_node",
        name="controller_node",
        parameters=[param_file],
        output="screen",
    )

    main_ui_node = Node(
        package="gesture_robot",
        executable="main_ui",
        name="main_ui",
        output="screen",
    )

    return LaunchDescription(
        [
            camera_node,
            gesture_node,
            object_tracking_node,
            controller_node,
            main_ui_node,
        ]
    )

