# Setup

## 전제 조건

- Ubuntu 24.04
- ROS2 Jazzy
- Python 3.12
- `colcon`, `rosdep`

## 의존성 설치

```bash
source /opt/ros/jazzy/setup.bash
cd ros2_ws
rosdep install --from-paths src --ignore-src -r -y
```

OpenCV와 MediaPipe 의존성은 실제 어댑터 구현 방식을 확정한 뒤 `package.xml` 또는
별도 Python 의존성 파일에 추가한다.

## 빌드

```bash
colcon build --symlink-install
source install/setup.bash
```

## 인터페이스 확인

```bash
ros2 interface show gesture_robot_interfaces/msg/GestureCommand
ros2 interface show gesture_robot_interfaces/msg/TrackedObject
python3 -c "from gesture_robot_interfaces.msg import GestureCommand, TrackedObject"
```

현재는 노드 실행 진입점이 등록되지 않았으므로 `ros2 run`과 전체 Launch 실행은 실제
노드 구현 이후 사용한다.
