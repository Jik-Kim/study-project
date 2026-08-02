from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    use_sim_time = LaunchConfiguration("use_sim_time", default="true")
    cmd_vel_topic = LaunchConfiguration("cmd_vel_topic", default="/cmd_vel")

    return LaunchDescription([
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="true",
            description="Use simulation (Gazebo) clock if true",
        ),
        DeclareLaunchArgument(
            "cmd_vel_topic",
            default_value="/cmd_vel",
            description="Target velocity topic for Gazebo robot",
        ),
        # 카메라 입력 노드
        Node(
            package="gesture_robot",
            executable="camera_node",
            name="camera_node",
            output="screen",
            parameters=[{"use_sim_time": use_sim_time}],
        ),
        # 제스처 인식 노드
        Node(
            package="gesture_robot",
            executable="gesture_node",
            name="gesture_node",
            output="screen",
            parameters=[{"use_sim_time": use_sim_time}],
        ),
        # 객체 추적 노드
        Node(
            package="gesture_robot",
            executable="object_tracking_node",
            name="object_tracking_node",
            output="screen",
            parameters=[{"use_sim_time": use_sim_time}],
        ),
        # 이동 제어 노드 (Gazebo의 /cmd_vel로 토픽 remapping 지원)
        Node(
            package="gesture_robot",
            executable="controller_node",
            name="controller_node",
            output="screen",
            parameters=[{"use_sim_time": use_sim_time}],
            remappings=[("turtle1/cmd_vel", cmd_vel_topic)],
        ),
        # 통합 시각화 UI 노드
        Node(
            package="gesture_robot",
            executable="main_ui",
            name="main_ui",
            output="screen",
            parameters=[{"use_sim_time": use_sim_time}],
        ),
    ])
