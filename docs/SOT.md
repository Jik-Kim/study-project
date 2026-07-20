# Source of Truth

> 상태: 팀 승인 대기 초안  
> 갱신일: 2026-07-11

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

PID, 다중 객체, Gazebo, 음성 명령은 MVP 완료 후 검토한다.

## 패키지 구조 결정

```text
ros2_ws/src/
├── gesture_robot_interfaces/  # ament_cmake + rosidl
└── gesture_robot/             # ament_python + rclpy
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

## 현재 확정 사항

- Python 3.12와 ROS2 Jazzy를 사용한다.
- 애플리케이션 노드는 `rclpy` 기반으로 작성한다.
- 공통 통신 계약은 별도 `ament_cmake + rosidl` 패키지에서 관리한다.
- rosidl이 생성한 Python 메시지를 애플리케이션에서 우선 사용한다.
- 향후 C++ 노드가 필요하면 동일한 rosidl 메시지의 C++ 코드를 사용할 수 있다.
- 제스처 인식은 MediaPipe Python API를 사용한다.
- 객체 추적은 OpenCV Python API의 HSV 색상 검출로 시작한다.
- 첫 번째 시뮬레이션은 turtlesim을 사용한다.
- 구현 전까지 파라미터 값과 실행 파일 등록은 TODO로 둔다.

## 초기 인터페이스 초안

- `GestureCommand.msg`: `header`, `command`, `confidence`
- `TrackedObject.msg`: `header`, `detected`, `error_x`, `error_y`, `area`

이 필드는 rosidl 빌드 구조를 검증하기 위한 최소 초안이다. 실제 구현 전에 팀이
필드 의미와 단위를 검토한다.

## 미결정 사항

- 제스처 명령의 상수와 허용값
- 토픽 이름과 QoS
- 추적 결과 필드의 단위와 추가 정보
- 로봇 속도 명령에 표준 `geometry_msgs/Twist`를 사용할지 여부
- 기본 추적 색상과 HSV 범위
- 카메라 공유 방식
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
