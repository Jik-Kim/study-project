# Feature Todo

실제 파일과 메서드를 기준으로 구현할 피처를 관리한다.

## 인터페이스 패키지

### `gesture_robot_interfaces/msg/GestureCommand.msg`

- [x] 제스처 명령 종류와 필드 확정

### `gesture_robot_interfaces/msg/TrackedObject.msg`

- [x] 위치 오차와 면적의 단위 확정
- [x] 객체 미검출 표현 방식 확정
- [ ] 위치 오차의 부호 규칙 확정

### `gesture_robot_interfaces/CMakeLists.txt`

- [x] 현재 MVP rosidl 메시지 생성 목록 반영

## ROS2 통신 계약

- [ ] 노드별 토픽 이름 합의 및 문서화
- [ ] 카메라·제어 명령 외 토픽의 QoS 합의

## 내부 모델

### `gesture_robot/core/models.py`

- [ ] 제스처 결과 모델 정의
- [ ] 객체 추적 결과 모델 정의
- [ ] 추적 상태와 이동 명령 모델 정의

## 객체 추적

### `gesture_robot/adapters/opencv_camera.py`

- [ ] `OpenCVCamera.open()`: 카메라 연결
- [ ] `OpenCVCamera.read()`: 프레임 읽기
- [ ] `OpenCVCamera.release()`: 카메라 자원 해제

### `gesture_robot/core/color_tracker.py`

- [ ] `ColorTracker.track()`: HSV 마스크와 객체 위치 계산
- [ ] `ColorTracker.track()`: 노이즈 및 미검출 처리

### `gesture_robot/visualization/tracking_visualizer.py`

- [ ] `TrackingVisualizer.render()`: 객체 위치와 상태 표시

### `gesture_robot/nodes/object_tracking_node.py`

- [ ] `ObjectTrackingNode.__init__()`: Publisher, Timer, 파라미터 구성
- [ ] `ObjectTrackingNode.process_frame()`: 추적 처리 흐름 연결
- [ ] `ObjectTrackingNode.publish_tracking_result()`: `TrackedObject` 발행

## 제스처 인식

### `gesture_robot/adapters/mediapipe_detector.py`

- [ ] `MediaPipeDetector.detect()`: 손 랜드마크 검출

### `gesture_robot/core/gesture_classifier.py`

- [ ] `GestureClassifier.classify()`: 시작·정지 제스처 분류
- [ ] `GestureClassifier.classify()`: 미인식 상태 처리

### `gesture_robot/nodes/gesture_node.py`

- [ ] `GestureNode.__init__()`: Publisher, Timer, 파라미터 구성
- [ ] `GestureNode.process_frame()`: 제스처 처리 흐름 연결
- [ ] `GestureNode.publish_gesture_command()`: `GestureCommand` 발행

## 상태 및 제어

### `gesture_robot/core/tracking_state.py`

- [ ] `TrackingStateMachine.update()`: 시작·정지 상태 전이
- [ ] `TrackingStateMachine.current_state()`: 현재 상태 반환

### `gesture_robot/core/tracking_controller.py`

- [ ] `TrackingController.calculate()`: 정지·전진·회전 명령 계산

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

## 실행 설정

### `gesture_robot/config/params.yaml`

- [ ] 노드별 파라미터 정의

### `gesture_robot/setup.py`

- [ ] 구현된 노드의 `console_scripts` 등록

### `gesture_robot/launch/gesture_robot.launch.py`

- [ ] `generate_launch_description()`: 노드와 파라미터 등록
