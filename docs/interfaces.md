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
| `command` | `uint8` | 인식된 제스처 명령 |
| `confidence` | `float32` | 인식 신뢰도 |

### 명령 상수

| 상수 | 값 | 의미 |
|---|---|---|
| `NONE` | 0 | 명령 없음 |
| `START` | 1 | 추적 시작 (보자기) |
| `STOP` | 2 | 추적 정지 (주먹) |

## `TrackedObject.msg`

| 필드 | 타입 | 의미 | 단위 |
|---|---|---|---|
| `detected` | `bool` | 객체 검출 여부 | - |
| `error_x` | `float32` | 화면 중심 기준 가로 오차 | 픽셀 |
| `error_y` | `float32` | 화면 중심 기준 세로 오차 | 픽셀 |
| `area` | `float32` | 검출 영역 면적 | px^2 |

### 미검출 처리

- `detected = False`일 때: `error_x`, `error_y`, `area`는 0
- 제어 노드는 `detected = False`일 때 정지 명령을 발행한다

## 토픽 계약

| 토픽 | 메시지 타입 | QoS | 설명 |
|---|---|---|---|
| `/gesture/command` | `GestureCommand` | RELIABLE | 제스처 인식 결과 |
| `/tracking/result` | `TrackedObject` | BEST_EFFORT | 객체 추적 결과 |
| `/turtle1/cmd_vel` | `geometry_msgs/Twist` | RELIABLE | 거북이 속도 명령 |

## 로봇 속도 명령

- 타입: `geometry_msgs/Twist`
- `linear.x`: 전진/후진 속도 (양수=전진)
- `angular.z`: 좌우 회전 속도 (양수=좌회전)

## 미정 사항

- 카메라 프레임 공유 방식
- HSV 범위 파라미터
