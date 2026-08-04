# Feature Todo

실제 파일과 메서드를 기준으로 구현할 피처를 관리한다.

## 인터페이스 패키지

### `gesture_robot_interfaces/msg/GestureCommand.msg`

- [x] 제스처 명령 종류와 필드 확정

### `gesture_robot_interfaces/msg/TrackedObject.msg`

- [x] 위치 오차와 면적의 단위 확정
- [x] 객체 미검출 표현 방식 확정
- [x] 위치 오차의 부호 규칙 확정

### `gesture_robot_interfaces/CMakeLists.txt`

- [x] 현재 MVP rosidl 메시지 생성 목록 반영

## ROS2 통신 계약

- [x] 노드별 토픽 이름 합의 및 문서화
- [x] 카메라·제어 명령 외 토픽의 QoS 합의

## 내부 모델

### `gesture_robot/core/models.py`

- [ ] 제스처 결과 모델 정의
- [ ] 객체 추적 결과 모델 정의
- [ ] 추적 상태와 이동 명령 모델 정의

## 객체 추적

### `gesture_robot/adapters/opencv_camera.py`

- [x] `OpenCVCamera.open()`: 카메라 연결
- [x] `OpenCVCamera.read()`: 프레임 읽기
- [x] `OpenCVCamera.release()`: 카메라 자원 해제

### `gesture_robot/nodes/camera_node.py`

- [x] `CameraNode.__init__()`: Publisher, Timer, 파라미터(device_id, publish_rate) 구성
- [x] `CameraNode._on_timer()`: 프레임 읽어 `camera/image_raw` 발행
- [x] `setup.py console_scripts` 등록

### `gesture_robot/core/color_tracker.py`

- [ ] `ColorTracker.track()`: HSV 마스크와 객체 위치 계산
- [ ] `ColorTracker.track()`: 노이즈 및 미검출 처리

### `gesture_robot/visualization/tracking_visualizer.py`

- [x] `TrackingVisualizer.render()`: 바운딩 박스·중심점·상태 텍스트 표시

### `gesture_robot/nodes/object_tracking_node.py`

- [x] `ObjectTrackingNode.__init__()`: Publisher, Timer, 파라미터 구성
- [x] `ObjectTrackingNode.process_frame()`: 추적 처리 흐름 연결
- [x] `ObjectTrackingNode.publish_tracking_result()`: `TrackedObject` 발행
- [x] 시각화된 프레임을 `camera/image_annotated`로 발행

## 제스처 인식

### `gesture_robot/adapters/mediapipe_detector.py`

- [ ] `MediaPipeDetector.detect()`: 손 랜드마크 검출

### `gesture_robot/core/gesture_classifier.py`

- [ ] `GestureClassifier.classify()`: 시작·정지 제스처 분류
- [ ] `GestureClassifier.classify()`: 미인식 상태 처리

### `gesture_robot/nodes/gesture_node.py`

- [x] `GestureNode.__init__()`: Publisher, Subscriber, 파라미터 구성
- [x] `GestureNode._image_callback()`: 제스처 처리 흐름 연결
- [x] `GestureNode.publish_gesture_command()`: `GestureCommand` 발행
- [x] 손 랜드마크를 그린 프레임을 `camera/image_annotated`로 발행

## 상태 및 제어

### `gesture_robot/core/tracking_state.py`

- [ ] `TrackingStateMachine.update()`: 시작·정지 상태 전이
- [ ] `TrackingStateMachine.current_state()`: 현재 상태 반환

### `gesture_robot/core/tracking_controller.py`

- [ ] `TrackingController.calculate()`: 정지·전진·회전 명령 계산
- [ ] 실제 카메라와 turtlesim 통합 테스트 후 이동 제어 파라미터 초깃값 확정

### `gesture_robot/nodes/controller_node.py`

- [ ] `ControllerNode.__init__()`: Subscriber와 Publisher 구성
- [ ] `ControllerNode.handle_gesture_command()`: 제스처 명령 소비
- [ ] `ControllerNode.handle_tracking_result()`: 추적 결과 소비
- [ ] `ControllerNode.publish_velocity_command()`: 이동 명령 발행

## 시뮬레이션

### `gesture_robot/adapters/turtlesim_adapter.py`

- [ ] `TurtlesimAdapter.apply_velocity()`: turtlesim 속도 연결

### `gesture_robot/nodes/simulation_node.py`

- [ ] `SimulationNode.__init__()`: 속도 Subscriber 구성
- [ ] `SimulationNode.handle_velocity_command()`: 이동 명령 전달

## UI

### `gesture_robot/ui/main_ui.py`

- [x] `MainUI._build_ui()`: Tkinter 창 및 레이아웃 구성
- [x] `MainUI._build_camera()`: 카메라 영역 배치
- [x] `MainUI._build_status()`: 상태 표시 영역 배치
- [x] `MainUI._build_simulation()`: 시뮬레이션 영역 배치
- [x] `MainUI._build_topic_flow()`: SOT 확정 4개 토픽 흐름 영역 배치
- [x] `MainUI._build_velocity()`: 속도값 실시간 그래프 영역 배치
- [x] `MainUI._tick()`: 모의 데이터로 UI 갱신 (상태·토픽 흐름·속도 그래프 포함)
- [x] `MainUI.update_camera_frame()`: ROS2 Subscribe 연동 후 실제 프레임 표시
- [x] `MainUI.update_status()`: ROS2 Topic 실시간 데이터로 갱신
- [x] `MainUI.update_topic_activity()`: 실제 노드 Publish 시점과 연동
- [x] `MainUI.update_velocity()`: `controller_node`가 발행한 실제 `Twist` 값으로 갱신
- [x] `use_mock` 플래그 추가 (standalone 테스트용 모의 모드 유지)

### `gesture_robot/nodes/main_ui_node.py` (신규)

- [x] `camera/image_annotated`, `gesture/command`, `tracking/object`, `turtle1/cmd_vel` 구독
- [x] MainUI의 update_* 메서드와 연결
- [x] `main()`: Tkinter mainloop와 rclpy spin 공존 처리, setup.py console_scripts 등록

## 손 위치 추적 데모 (turtlesim/Gazebo)

실제 공 없이 손 위치만으로 turtlesim/Gazebo 추적을 시연하기 위한 보조 기능.
`controller_node`/`tracking_controller.py`(실제 공·카메라-온-로봇 전제)는
건드리지 않고 별도 노드로 구성했다. 이 노드들은 `controller_node`와 동시에
실행하면 안 된다(같은 cmd_vel 토픽 충돌).

### `gesture_robot/nodes/gesture_node.py` (추가)

- [x] 손 랜드마크 중심 좌표를 `TrackedObject`로 변환해 `tracking/object`에 발행
  (`hand_area_scale` 파라미터로 공 기준 스케일에 맞춤)
- [x] START(편 손)일 때만 detected=True, STOP/NONE(주먹·미검출)이면
  detected=False로 발행해 추적 대상이 사라진 것처럼 동작

### `gesture_robot/nodes/camera_node.py` (추가)

- [x] `mirror` 파라미터로 좌우 반전(셀카 모드) 지원

### `gesture_robot/core/pursuit_controller.py` (신규)

- [x] `PursuitController.calculate()`: 로봇의 실제 pose와 목표 좌표로 추적
  속도 계산 (화면 오차가 아닌 절대 좌표 기반, turtlesim/Gazebo 공용)

### `gesture_robot/nodes/target_marker_node.py` (신규)

- [x] turtlesim에 `target` turtle을 스폰해 손 위치를 순간이동으로 표시

### `gesture_robot/nodes/turtle_pursuit_node.py` (신규)

- [x] `/turtle1/pose`, `/target/pose`, `gesture/command`로 turtle1이 target을
  실제로 추적하도록 `cmd_vel` 발행, 제스처 STOP 시 즉시 정지

### `gesture_robot/nodes/gazebo_pursuit_node.py` (신규)

- [x] `/odom`, `tracking/object`, `gesture/command`로 turtlebot3(Gazebo)가
  손 위치를 추적하도록 `cmd_vel` 발행

### `sim_bringup/config/topdown_gui.config` (신규)

- [x] Gazebo GUI 카메라를 탑뷰로 설정 (SDF `<gui><camera>`는 이 gz-sim
  버전에서 미지원이라 별도 GUI 플러그인 설정 파일 사용)

### `sim_bringup/models/turtlebot3_burger_big.sdf` (신규)

- [x] 화면 가시성을 위해 시각적 크기만 2배로 키운 burger 모델
  (충돌/관성 등 물리 속성은 원본과 동일)

## 실행 설정

### `gesture_robot/config/params.yaml`

- [ ] 노드별 파라미터 정의

### `gesture_robot/setup.py`

- [ ] 구현된 노드의 `console_scripts` 등록

### `gesture_robot/launch/gesture_robot.launch.py`

- [ ] `generate_launch_description()`: 노드와 파라미터 등록
