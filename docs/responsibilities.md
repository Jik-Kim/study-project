# 프로젝트 구조와 영역별 책임

## 전체 프로젝트 구조

```text
team_proj/
├── AGENTS.md                     # Codex 공통 작업 규칙
├── PROJECT.md                    # 프로젝트 개요
├── README.md                     # 프로젝트 시작 안내
├── docs/
│   ├── SOT.md                    # 프로젝트 최상위 기준 문서
│   ├── architecture.md           # 시스템 데이터 흐름
│   ├── interfaces.md             # ROS2 메시지와 토픽 계약
│   ├── responsibilities.md       # 영역별 역할과 책임
│   ├── setup.md                  # 개발 환경과 빌드 방법
│   └── todo.md                   # 파일·메서드 기반 피처 목록
└── ros2_ws/
    └── src/
        ├── gesture_robot_interfaces/
        │   ├── msg/
        │   │   ├── GestureCommand.msg
        │   │   └── TrackedObject.msg
        │   ├── CMakeLists.txt
        │   └── package.xml
        ├── gesture_robot/
        │   ├── gesture_robot/
        │   │   ├── nodes/
        │   │   ├── core/
        │   │   ├── adapters/
        │   │   └── visualization/
        │   ├── config/
        │   │   └── params.yaml
        │   ├── launch/
        │   │   └── gesture_robot.launch.py
        │   ├── resource/
        │   ├── package.xml
        │   ├── setup.py
        │   └── setup.cfg
        └── sim_bringup/
            ├── CMakeLists.txt
            └── package.xml
```

## `gesture_robot_interfaces` 패키지

ROS2 노드 사이에서 사용할 공통 메시지 형식을 정의한다. rosidl을 이용해 `.msg`
파일에서 Python과 C++ 메시지 코드를 생성한다.

### `msg`

제스처 명령과 객체 추적 결과처럼 노드 사이에서 교환할 데이터 구조를 정의한다.

### `CMakeLists.txt`

rosidl 메시지 생성 대상과 필요한 빌드 설정을 관리한다.

### `package.xml`

인터페이스 패키지의 정보와 ROS2 의존성을 선언한다.

## `gesture_robot` 패키지

제스처 인식, 객체 추적, 상태 관리, 이동 제어와 시뮬레이션을 담당하는 Python ROS2
애플리케이션이다.

### `nodes`

Publisher, Subscriber, Timer, Parameter를 구성하고 각 기능의 실행 순서를 조율한다.

### `core`

색상 추적, 제스처 분류, 추적 상태와 이동 제어 같은 핵심 판단 및 계산을 담당한다.
가능한 한 ROS2와 외부 라이브러리에 직접 의존하지 않는다.

### `adapters`

OpenCV 카메라, MediaPipe, turtlesim 같은 외부 라이브러리와 장치를 내부 코드에
연결한다.

### `visualization`

객체 위치, 검출 여부, 추적 상태와 디버깅 정보를 화면에 표시한다.

### `config`

카메라, HSV 색상 범위, 제어 값처럼 실행 중 조절할 ROS2 파라미터를 관리한다.

### `launch`

여러 ROS2 노드와 파라미터를 하나의 명령으로 실행할 수 있도록 구성한다.

### `setup.py`, `setup.cfg`, `resource`

Python 모듈과 실행 파일을 ROS2 패키지로 설치하고 검색할 수 있도록 구성한다.

### `package.xml`

애플리케이션 패키지 정보와 `rclpy`, 인터페이스 패키지 등의 의존성을 선언한다.

## `sim_bringup` 패키지

turtlesim 실행과 전체 통합에 필요한 launch 파일을 관리한다. Gazebo 확장은
통합 테스트 후 선택하며, 선택 전에는 Gazebo 의존성을 추가하지 않는다.

## 패키지 연결 관계

### 프로젝트 처리 흐름

```text
[gesture_robot/adapters]
손 랜드마크 검출
  ↓
[gesture_robot/core]
추적 시작 제스처 분류
  ↓
[gesture_robot/nodes + gesture_robot_interfaces]
GestureCommand 메시지 발행
  ↓
[gesture_robot/nodes → core]
메시지 구독 및 추적 상태 활성화
  ↓
[gesture_robot/adapters → core]
카메라 입력 및 색상 객체 위치 계산
  ↓
[gesture_robot/nodes + gesture_robot_interfaces]
TrackedObject 메시지 발행
  ↓
[gesture_robot/nodes → core]
메시지 구독 및 이동 명령 계산
  ↓
[gesture_robot/nodes → adapters]
이동 명령을 turtlesim에 전달
```

### 실생활 예시: 카페 주문

```text
[Adapter]
직원이 고객의 주문을 접수
  ↓
[Core]
주문의 의미와 처리 방법 판단
  ↓
[Interface]
정해진 주문서 양식으로 작성
  ↓
[Node / Publisher]
주문 완료 신호를 주방에 전달
  ↓
[Node / Subscriber]
주방이 주문 신호를 수신
  ↓
[Core]
주문에 맞는 제조 과정 결정
  ↓
[Adapter]
커피 머신과 외부 장비 작동
  ↓
[Visualization]
주문 상태를 전광판에 표시
```
