# Python application package rules

이 규칙은 `gesture_robot` 애플리케이션 패키지 전체에 적용된다.

## 책임과 경계

- ROS2 노드는 `rclpy`와 `gesture_robot_interfaces`의 생성 메시지를 사용한다.
- `nodes`에는 Publisher, Subscriber, Timer, 파라미터 처리와 호출 순서만 둔다.
- `core`에는 제스처 분류, 객체 추적, 상태 및 제어 알고리즘을 둔다.
- `adapters`에는 OpenCV, MediaPipe, 카메라, turtlesim 연결 코드를 둔다.
- `visualization`에는 화면 출력과 디버깅 시각화 코드를 둔다.
- `core`는 가능한 한 `rclpy`, OpenCV, MediaPipe에 직접 의존하지 않는다.

## 구현 규칙

- 노드 경계에서 내부 Python 모델과 rosidl 메시지를 변환한다.
- 카메라와 외부 자원은 실패 처리와 명시적인 해제 경로를 갖게 한다.
- 파라미터 기본값과 YAML 값은 인터페이스 합의 후 추가한다.
- 노드 `main()` 구현 후에만 `setup.py`의 `console_scripts`에 등록한다.
- 실행 가능한 노드만 Launch 파일에 등록한다.

## 검증

- 변경한 Python 파일의 구문 검사와 관련 단위 테스트를 실행한다.
- 패키징 또는 ROS2 통신 변경 후 전체 워크스페이스를 빌드한다.
- 노드 실행 항목 추가 후 `ros2 run` 또는 Launch 실행을 확인한다.
