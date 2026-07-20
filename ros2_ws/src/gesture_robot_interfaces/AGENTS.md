# Interface package rules

이 규칙은 `gesture_robot_interfaces` 패키지 전체에 적용된다.

## 책임과 경계

- 이 패키지에는 `.msg`, `.srv`, `.action`과 생성에 필요한 CMake 설정만 둔다.
- 노드, 알고리즘, OpenCV, MediaPipe, UI 코드를 넣지 않는다.
- 애플리케이션 패키지를 의존하지 않는다.
- 기존 ROS2 표준 메시지로 충분한지 확인한 뒤 커스텀 인터페이스를 추가한다.

## 인터페이스 변경

- 필드 이름은 의미가 분명해야 하며 단위와 유효 범위를 문서화한다.
- 필드 추가, 삭제, 타입 변경이 기존 노드에 미치는 영향을 먼저 확인한다.
- 메시지 변경 시 `docs/interfaces.md`와 `docs/SOT.md`를 함께 갱신한다.
- 확정되지 않은 필드는 추측해서 추가하지 않고 TODO로 남긴다.

## 검증

- 워크스페이스 루트에서 `colcon build --symlink-install`을 실행한다.
- `ros2 interface show gesture_robot_interfaces/msg/<MessageName>`으로 결과를 확인한다.
- 생성된 메시지의 Python import를 확인한다.
