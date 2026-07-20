# Architecture

## 패키지 관계

```text
gesture_robot_interfaces
        │ rosidl이 생성한 Python 메시지
        ▼
gesture_robot (rclpy)
```

`gesture_robot_interfaces`를 먼저 빌드하면 rosidl이 Python과 C++ 메시지 코드를
생성한다. 현재 애플리케이션은 생성된 Python 메시지를 import하여 사용한다.

## 데이터 흐름

```text
gesture_node ── GestureCommand ─────────┐
                                       ▼
object_tracking_node ─ TrackedObject ─ controller_node ─ 속도 명령 ─ simulation_node
```

## 애플리케이션 내부 구조

```text
nodes ──→ core
  │       ↑
  ├──→ adapters
  └──→ visualization
```

- `nodes`: rclpy 통신, rosidl 메시지 변환, 메서드 호출 순서
- `core`: 프레임워크 독립 Python 알고리즘
- `adapters`: OpenCV, MediaPipe, 시뮬레이터 연결
- `visualization`: OpenCV 화면 출력

현재 노드 파일에는 호출 순서만 있으며 실제 Publisher, Subscriber, `main()`은 TODO다.
