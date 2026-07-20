# Interfaces

인터페이스 정의는 `gesture_robot_interfaces/msg`가 실제 기준이며, 이 문서는 필드의
의도와 미결정 사항을 설명한다.

rosidl 빌드 후 Python 노드는 다음 경로에서 생성 메시지를 가져온다.

```python
from gesture_robot_interfaces.msg import GestureCommand, TrackedObject
```

## `GestureCommand.msg`

| 필드 | 의미 |
|---|---|
| `header` | 생성 시각과 좌표계 정보 |
| `command` | 인식된 제스처 명령 |
| `confidence` | 인식 신뢰도 |

[x]TODO: 명령 문자열을 유지할지 `uint8` 상수로 변경할지 결정한다.
## `GestureCommand.msg`

| 필드 | 의미 |
|---|---|
| `header` | 생성 시각과 좌표계 정보 |
| `command` | 인식된 제스처 명령 (`uint8` 상수 사용: `NONE=0`, `START=1`, `STOP=2`) |
| `confidence` | 인식 신뢰도 |

- **상수값 정의:** `NONE=0`, `START=1`, `STOP=2` (2주차 회의 결과 반영 완료)

## `TrackedObject.msg`

| 필드 | 의미 |
|---|---|
| `header` | 생성 시각과 좌표계 정보 |
| `detected` | 객체 검출 여부 |
| `error_x` | 화면 중심 기준 가로 오차 |
| `error_y` | 화면 중심 기준 세로 오차 |
| `area` | 검출 영역 면적 |

TODO: 각 수치의 단위, 미검출 시 값, 화면 크기 필드 필요 여부를 결정한다.

## 미정 인터페이스

## 임시 통신 규격 및 검증 기록 (1차)

- **임시 토픽 이름:** `/gesture/command` (테스트용 임시 지정)
- **검증 내용:** `test_publisher.py`와 `test_subscriber.py` 노드를 통해 `/gesture/command` 토픽으로 `START(1)` 명령 및 신뢰도(`confidence: 0.95`) 정상 송수신 확인 완료 (2026-07-20, 이시율)

## 미정 인터페이스

- 정식 토픽 이름 확정
- QoS 설정
- 로봇 속도 명령 타입
- 카메라 프레임 공유 방식

