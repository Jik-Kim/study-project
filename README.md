# 제스처 제어 기반 객체 추적 로봇 시스템

MediaPipe와 OpenCV로 제스처 및 색상 객체를 인식하고, ROS2 Python 노드로
시뮬레이션 로봇을 제어하는 입문 프로젝트입니다.

## 프로젝트 정보

- 기간: 2026-07-10 ~ 2026-08-05
- 팀원: 김병직, 김도윤, 황인재, 조정묵, 이시율
- 기술 방향: Python 3.12, ROS2 Jazzy, rclpy, rosidl, OpenCV, MediaPipe

## 기준 문서

- [프로젝트 SOT](docs/SOT.md)
- [영역별 책임](docs/responsibilities.md)
- [아키텍처](docs/architecture.md)
- [인터페이스](docs/interfaces.md)
- [개발 환경](docs/setup.md)
- [작업 목록](docs/todo.md)

## 프로젝트 구조

```text
ros2_ws/src/
├── gesture_robot_interfaces/  # ament_cmake + rosidl 메시지 계약
├── gesture_robot/             # ament_python + rclpy 애플리케이션
│   ├── gesture_robot/
│   ├── config/
│   ├── launch/
│   ├── setup.py
│   ├── setup.cfg
│   └── package.xml
└── sim_bringup/               # turtlesim 및 통합 launch
```

## 빌드

```bash
source /opt/ros/jazzy/setup.bash
cd ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

현재는 구조와 메서드 호출 관계만 정의한 골격 단계입니다. 실제 알고리즘, rclpy
Publisher/Subscriber, 실행 진입점과 Launch 등록은 TODO로 남겨져 있습니다.
