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

## 주요 기능

- **제스처 인식 (MediaPipe)**: 손 보자기를 `START`(추적 시작), 주먹을 `STOP`(추적 정지) 명령으로 변환
- **객체 추적 (OpenCV)**: HSV 색상 영역(기본: 빨간 공) 및 손 중심 좌표 추적
- **시뮬레이션 로봇 제어**: `turtlesim` 2D MVP 및 `Gazebo` 3D (TurtleBot3) 자율 추적 제어
- **ROS2 노드 간 커스텀 통신**: rosidl 기반 `GestureCommand`, `TrackedObject` 토픽 발행
- **통합 모니터링 UI (`main_ui`)**: 카메라 영상/랜드마크, 토픽 활성 상태, 속도 실시간 그래프, 수치 모니터링 제공

## 빌드 및 실행

### 1. Python 의존성 설치
```bash
pip install --break-system-packages "numpy==1.26.4" "mediapipe==0.10.14"
```

### 2. 패키지 빌드 및 환경 로드
```bash
cd ros2_ws
colcon build --symlink-install
source install/setup.bash
```

### 3. 시뮬레이션 실행

- **turtlesim 2D MVP 실행**:
  ```bash
  ros2 launch sim_bringup turtlesim_bringup.launch.py
  ```
- **Gazebo 3D 시뮬레이션 실행**:
  ```bash
  ros2 launch sim_bringup gazebo_bringup.launch.py
  ```
