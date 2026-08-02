# Architecture

## 패키지 관계

```text
gesture_robot_interfaces
        │ rosidl이 생성한 Python 메시지
        ▼
gesture_robot (rclpy)

sim_bringup (turtlesim 실행·통합 launch)
```

`gesture_robot_interfaces`를 먼저 빌드하면 rosidl이 Python과 C++ 메시지 코드를
생성한다. 현재 애플리케이션은 생성된 Python 메시지를 import하여 사용한다.

## 데이터 흐름

```text
camera_node ── /camera/image_raw ─┬─ gesture_node
                                 │       └─ /gesture/command ─┐
                                 └─ object_tracking_node      │
                                      └─ /tracking/object ────┤
                                                              ▼
                                                       controller_node
                                                              │
                                                     /turtle1/cmd_vel
                                                              ▼
                                                         turtlesim
```

거북이에 전방 카메라가 장착된 것으로 가정한다. 제어 노드는 다음 입력 관계로
turtlesim의 속도를 계산한다.

```text
error_x ───────────────→ angular.z
target_area - area ────→ linear.x
error_y ───────────────→ 시각화·향후 확장
GestureCommand ────────→ 추적 START/STOP 상태
```

객체가 미검출되면 속도 0을 발행하되 추적 상태는 유지한다. 객체가 다시 검출되었을
때 기존 상태가 START이면 이동을 재개한다.

## 애플리케이션 내부 구조

```text
nodes ──→ core
  │       ↑
  ├──→ adapters
  ├──→ visualization
  └──→ ui
```

- `nodes`: rclpy 통신, rosidl 메시지 변환, 메서드 호출 순서
- `core`: 프레임워크 독립 Python 알고리즘
- `adapters`: OpenCV, MediaPipe, 시뮬레이터 연결
- `visualization`: OpenCV 프레임 위에 검출 결과를 그려 넣는 오버레이 렌더링
- `ui`: Tkinter 통합 실행 창 조립과 패널 배치(카메라·상태·시뮬레이션·토픽 흐름·속도
  그래프), `visualization`이 만든 프레임과 `nodes`가 전달한 상태값을 화면에 표시

`simulation_node`는 아직 구현이 남아 있다(controller_node가 `turtle1/cmd_vel`을 직접
발행해 turtlesim 기준으로는 별도 구현이 필요 없을 수 있음, 팀 논의 필요).
`camera_node`, `gesture_node`, `object_tracking_node`, `controller_node`는 구현되어
있으며, 실제 웹캠·turtlesim·Gazebo 환경에서의 전체 통합 검증이 필요하다.
