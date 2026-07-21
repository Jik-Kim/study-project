# Interfaces

인터페이스 정의는 `gesture_robot_interfaces/msg`가 실제 기준이며, 이 문서는 필드의
의도와 미결정 사항을 설명한다.

rosidl 빌드 후 Python 노드는 다음 경로에서 생성 메시지를 가져온다.

```python
from gesture_robot_interfaces.msg import GestureCommand, TrackedObject
```

## `GestureCommand.msg`

| 필드 | 타입 | 의미 |
|---|---|---|
| `header` | `std_msgs/Header` | 생성 시각과 좌표계 정보 |
| `command` | `uint8` | 인식된 제스처 명령 |
| `confidence` | `float32` | 인식 신뢰도 |

| 상수 | 값 | 의미 |
|---|---|---|
| `NONE` | `0` | 손 미검출 또는 명령 없음. 기존 추적 상태 유지 |
| `START` | `1` | 보자기 제스처. 추적 시작 |
| `STOP` | `2` | 주먹 제스처. 추적 정지 |

## `TrackedObject.msg`

| 필드 | 타입 | 단위 | 의미 |
|---|---|---|---|
| `header` | `std_msgs/Header` | - | 생성 시각과 좌표계 정보 |
| `detected` | `bool` | - | 객체 검출 여부 |
| `error_x` | `float32` | 픽셀 | 화면 중심과 공 중심 사이의 가로 오차 |
| `error_y` | `float32` | 픽셀 | 화면 중심과 공 중심 사이의 세로 오차 |
| `area` | `float32` | 픽셀² | 검출된 공의 면적 |

객체가 검출되지 않으면 `detected = false`로 알린다. 제어 노드는 이
값을 받으면 거북이를 정지시킨다.

## 속도 명령

- 메시지 타입은 `geometry_msgs/Twist`를 사용한다.
- 공의 면적이 클수록 전진 속도를 높인다.
- 면적-속도 변환 gain과 최대 속도는 추가 합의 후 ROS2 파라미터로
  관리한다.

## QoS 원칙

- 정지 신호와 제어 명령은 RELIABLE을 사용한다.
- 카메라 영상은 BEST_EFFORT를 사용한다.

## 미정 인터페이스

- 노드별 구체적인 토픽 이름
- 카메라·제어 명령 외 토픽의 QoS
- `error_x`, `error_y`의 부호 규칙
