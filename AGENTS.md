# AGENTS.md

## 작업 기준

작업 전에 `docs/SOT.md`를 확인한다. 문서와 코드가 충돌하면 승인된 최신 SOT를
우선하고, 인터페이스 변경은 SOT와 `docs/interfaces.md`에 함께 반영한다.

## 패키지 규칙

- `gesture_robot_interfaces`는 rosidl 인터페이스 전용 `ament_cmake` 패키지다.
- `gesture_robot`은 rclpy 애플리케이션 `ament_python` 패키지다.
- 인터페이스 패키지에 알고리즘이나 노드 코드를 넣지 않는다.
- `nodes`는 rclpy 통신과 호출 순서만 담당한다.
- `core`는 제스처, 추적, 상태 및 제어 알고리즘을 담당한다.
- `adapters`는 카메라, MediaPipe, 시뮬레이터 연동을 담당한다.
- `visualization`은 화면 출력을 담당한다.
- 구현되지 않은 영역은 임의의 값으로 채우지 않고 한글 TODO로 남긴다.

## 코드 규칙

- 변수와 함수는 `snake_case`, 클래스는 `PascalCase`, 상수는 `UPPER_CASE`를 쓴다.
- 들여쓰기는 공백 4칸을 사용한다.
- `core`는 가능한 한 `rclpy`, OpenCV, MediaPipe에 직접 의존하지 않는다.
- 노드 간 직접 함수 호출 대신 rosidl 메시지를 이용한 토픽 통신을 적용한다.

## 검증

- Python 구문 검사를 수행한다.
- `colcon build --symlink-install`로 전체 워크스페이스 빌드를 확인한다.
- 인터페이스 변경 후 `ros2 interface show`와 Python import를 확인한다.
- 기존 사용자 변경 사항과 무관한 파일을 되돌리지 않는다.
