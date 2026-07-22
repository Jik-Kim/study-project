# Source of Truth

> 상태: 팀 합의 반영
> 갱신일: 2026-07-22

이 문서는 프로젝트의 현재 방향과 합의된 결정을 관리한다. 회의록 원문은 Notion에서
관리하고, 팀에서 확정한 내용만 이 문서에 반영한다.

## 프로젝트 목표

ROS2의 Node, Topic, rosidl Interface, Parameter, Launch를 학습하면서 제스처 제어
기반 객체 추적 시스템을 완성한다.

## MVP

- 손 제스처 인식
- HSV 색상 객체 위치 추적
- 제스처에 따른 추적 시작 및 정지
- rosidl 메시지를 이용한 노드 간 통신
- turtlesim 기반 로봇 제어
- 추적 결과 시각화

최종 MVP 시뮬레이터는 turtlesim으로 확정한다. PID, 다중 객체, 음성 명령은 MVP
완료 후 검토하고, Gazebo 확장은 전체 통합 테스트 과정에서 선택한다.

거북이에 전방 카메라가 장착된 것으로 가정한다. 화면에서 공이 왼쪽에 있으면
거북이가 왼쪽으로, 오른쪽에 있으면 오른쪽으로 회전한다. 공이 멀어 작게 보일수록
빠르게 전진하고, 목표 면적에 가까워질수록 감속한다.

## 패키지 구조 결정

```text
ros2_ws/src/
├── gesture_robot_interfaces/  # ament_cmake + rosidl
├── gesture_robot/             # ament_python + rclpy
└── sim_bringup/               # 시뮬레이터 관련 launch
```

### `gesture_robot_interfaces`

- `.msg`, `.srv`, `.action` 같은 노드 간 데이터 계약만 관리한다.
- `rosidl_generate_interfaces()`로 Python과 C++ 메시지 코드를 생성한다.
- 알고리즘, 노드, 장치 연결 코드를 포함하지 않는다.

### `gesture_robot`

| 영역 | 책임 |
|---|---|
| `nodes` | rclpy 통신, rosidl 메시지 변환, 기능 호출 순서 |
| `core` | 제스처, 객체 추적, 상태, 제어 알고리즘 |
| `adapters` | OpenCV 카메라, MediaPipe, 시뮬레이터 연결 |
| `visualization` | 영상 및 상태 시각화 |
| `config` | ROS2 파라미터 설정 |
| `launch` | 여러 노드의 통합 실행 |

`core`는 가능한 한 ROS2와 외부 라이브러리에 직접 의존하지 않는다. 노드는 내부
Python 데이터와 rosidl 메시지 사이의 변환 및 호출 순서를 담당한다.

### `sim_bringup`

- turtlesim 및 선택적 Gazebo 확장에 필요한 launch 파일을 한 패키지에서 관리한다.
- Gazebo를 최종 발표에 포함할지는 통합 테스트 결과 후 결정한다.

## 현재 확정 사항

- Python 3.12와 ROS2 Jazzy를 사용한다.
- 애플리케이션 노드는 `rclpy` 기반으로 작성한다.
- 공통 통신 계약은 별도 `ament_cmake + rosidl` 패키지에서 관리한다.
- rosidl이 생성한 Python 메시지를 애플리케이션에서 우선 사용한다.
- 향후 C++ 노드가 필요하면 동일한 rosidl 메시지의 C++ 코드를 사용할 수 있다.
- 제스처 인식은 MediaPipe Python API를 사용한다.
- 제스처 명령은 보자기를 추적 시작, 주먹을 추적 정지로 해석한다.
- 객체 추적은 OpenCV Python API의 HSV 색상 검출로 시작하며 기본
  추적 대상은 빨간 공으로 한다.
- 카메라 입력은 단일 카메라 노드가 프레임을 공유하는 구조로 한다.
- 속도 명령은 `geometry_msgs/Twist`를 사용한다.
- 제스처와 속도 명령은 RELIABLE, 카메라 영상과 객체 추적 결과는 BEST_EFFORT
  QoS를 사용한다.
- 최종 MVP 시뮬레이션은 turtlesim을 사용한다.

## 공통 인터페이스 계약

### `GestureCommand.msg`

```text
std_msgs/Header header

uint8 NONE=0
uint8 START=1
uint8 STOP=2

uint8 command
float32 confidence
```

- 손이 검출되지 않으면 `NONE`을 발행한다.
- `NONE`은 추적 상태를 바꾸지 않으며 마지막 `START` 또는 `STOP` 상태를
  유지한다.

### `TrackedObject.msg`

- 필드는 `header`, `detected`, `error_x`, `error_y`, `area`를 사용한다.
- `error_x`, `error_y`는 `object_center - image_center`로 계산한 픽셀 오차다.
- 화면 오른쪽은 `error_x > 0`, 왼쪽은 `error_x < 0`으로 정의한다.
- 화면 아래쪽은 `error_y > 0`, 위쪽은 `error_y < 0`으로 정의한다.
- `error_x`는 좌우 회전에 사용한다. `error_y`는 MVP 이동 제어에는 사용하지 않고
  시각화와 향후 확장을 위해 유지한다.
- `area`는 검출된 공의 픽셀 면적이며 거리의 근삿값으로 사용한다.
- 객체 미검출 시 `detected = false`로 제어 노드에 알리고 거북이를
  정지시킨다. 이때 제스처로 결정된 추적 상태는 유지한다.

### 토픽과 QoS

| 토픽 | 메시지 | QoS |
|---|---|---|
| `/camera/image_raw` | `sensor_msgs/Image` | BEST_EFFORT, KEEP_LAST, Depth 1 |
| `/gesture/command` | `GestureCommand` | RELIABLE |
| `/tracking/object` | `TrackedObject` | BEST_EFFORT, KEEP_LAST, Depth 1 |
| `/turtle1/cmd_vel` | `geometry_msgs/Twist` | RELIABLE |

- 노드 구현에서는 상대 토픽 이름을 사용하고, 문서에는 루트 namespace 기준의
  전체 토픽 이름을 표기한다.
- MVP에서는 별도 namespace와 remapping을 사용하지 않는다.

## 이동 제어 계약

- 회전 속도는 `angular_z = -angular_gain * error_x`로 계산한다.
- 화면 중앙 부근에는 `angular_deadband`를 적용하고 각속도를
  `max_angular_speed` 범위로 제한한다.
- 전진 속도는 `linear_x = linear_gain * (target_area - area)`로 계산한다.
- 목표 면적 부근에는 `area_deadband`를 적용하고 선속도를
  `max_linear_speed` 범위로 제한한다.
- 목표 면적보다 공이 크게 검출되면 MVP에서는 후진하지 않고 정지한다.
- `STOP`, 객체 미검출 또는 추적 결과 timeout 시 즉시 속도 0을 발행한다.
- 객체가 다시 검출되면 기존 추적 상태가 START인 경우 이동을 재개한다.

## 객체 추적 파라미터

- 빨간은 OpenCV HSV Hue `0~10`, `170~179` 두 구간의 마스크를 합쳐
  검출한다.
- Saturation과 Value의 초깃값은 각각 `100~255`로 한다.
- 최소 검출 면적의 초깃값은 `500.0` 픽셀²로 한다.
- morphology kernel 크기의 초깃값은 `5 x 5`로 한다.
- 카메라 장치 번호의 기본값은 `0`, 처리 주기는 `30 Hz`로 한다.
- HSV 범위, 최소 검출 면적, morphology kernel 크기, 카메라 장치 번호와
  처리 주기는 ROS2 파라미터로 관리한다.
- 객체 추적 파라미터 초깃값은 실제 카메라와 조명 환경에서 보정한다.

## 이동 제어 파라미터

- 파라미터 이름은 `linear_gain`, `angular_gain`, `target_area`,
  `area_deadband`, `angular_deadband`, `max_linear_speed`,
  `max_angular_speed`, `tracking_timeout_sec`를 사용한다.
- 수치 초깃값은 실제 카메라와 turtlesim 통합 테스트 후 확정한다.

## 역할과 리뷰 담당

| 기능 | 주 담당 | 리뷰 담당 | 1차 완료 기준 |
|---|---|---|---|
| 제스처 인식 | 조정묵 | 김도윤 | 카메라 입력에서 합의된 2~3개 명령과 신뢰도 출력 |
| 객체 추적 | 김병직 | 조정묵 | 지정 색상의 검출 여부와 위치 오차 출력 |
| 상태 및 이동 제어 | 황인재 | 김병직 | 추적 오차와 상태 입력으로 turtlesim 제어 |
| ROS2 통신 및 인터페이스 | 이시율 | 황인재 | 메시지 빌드, 최소 Pub/Sub, 기능 노드 통신 골격 연결 |
| 통합·시각화·검증 | 김도윤 | 이시율 | 한 명령으로 전체 실행 및 결과 화면·기본 동작 재현 |

- 각 담당자는 입력부터 출력까지 검증 가능한 기능 단위와 최소
  테스트를 함께 책임진다.
- 통합 담당자는 전체 launch, 공통 파라미터, 시각화, 통합 테스트,
  실행 문서, 데모 시나리오와 장애 대응 절차를 관리한다.

## 통합 화면과 데모

기본 실행 UI는 다음 네 가지 화면을 제공한다.

- turtlesim 시뮬레이션 창
- 웹캠 영상, 바운딩 박스, 제스처와 추적 상태 텍스트
- 노드와 토픽 흐름
- 속도값 실시간 그래프

## 미결정 사항

- 이동 제어 파라미터의 수치 초깃값
- Gazebo의 최종 발표 포함 여부

미결정 사항은 코드에 임의로 확정하지 않고 TODO로 남긴 뒤 팀 합의 후 반영한다.

## 데이터 및 문서 관리

- 논의 과정은 Notion, 확정된 결정은 이 SOT에서 관리한다.
- 대용량 이미지와 영상은 Git에 저장하지 않는다.
- 공유 데이터는 외부 객체 저장소에 두고 위치와 버전만 문서화한다.
- 소형 테스트 샘플만 필요할 때 `test/fixtures`에 추가한다.

## 변경 원칙

- MVP, 패키지 경계, rosidl 인터페이스 변경은 팀 합의가 필요하다.
- 메시지 변경 시 `msg` 파일, `docs/interfaces.md`, 이 SOT를 함께 수정한다.
- 세부 구현은 담당자가 진행하되 다른 영역과 맞닿는 변경은 먼저 공유한다.
- 기능별 브랜치와 Pull Request를 사용하고 지정된 리뷰 담당자가
  확인한다.
- Pull Request에는 실행 또는 테스트 방법을 기록한다.
- 공통 메시지, 토픽, QoS, 패키지 구조는 개인이 임의로 변경하지
  않고 작업 전에 팀에 공유한다.
