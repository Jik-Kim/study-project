# 프로젝트 골격 작업 요약

> 갱신일: 2026-07-11

## 최종 구조

```text
ros2_ws/src/
├── gesture_robot_interfaces/  # ament_cmake + rosidl
└── gesture_robot/             # ament_python + rclpy
```

## 인터페이스 패키지

- `GestureCommand.msg`와 `TrackedObject.msg` 초안
- `rosidl_generate_interfaces()` 설정
- colcon 빌드 시 Python과 C++ 메시지 코드 생성

## 애플리케이션 패키지

- `setup.py`, `setup.cfg`, `package.xml` 기반 Python 패키지
- `nodes`: rclpy 통신과 메서드 호출 순서
- `core`: 실제 알고리즘 TODO
- `adapters`: OpenCV, MediaPipe, turtlesim 연동 TODO
- `visualization`: 화면 출력 TODO

## 현재 구현 수준

- 노드에는 각 컴포넌트의 메서드 호출 관계만 정의했다.
- 개별 구현은 한글 TODO와 `NotImplementedError`로 남겼다.
- rclpy Publisher/Subscriber, 노드 `main()`, 파라미터 값, Launch 등록은 TODO다.
- rosidl 메시지는 생성되지만 필드와 단위는 팀 검토 전 초안이다.

## 다음 단계

1. 메시지 필드, 토픽 이름, 단위를 팀에서 확정한다.
2. 담당자별로 core와 adapter 구현을 진행한다.
3. rclpy Publisher와 Subscriber를 구현한다.
4. 노드 실행 항목과 Launch를 등록한다.

## Launch 참고

`generate_launch_description()`은 실행할 노드와 파라미터 목록을 ROS2 Launch에
반환한다. 현재는 실행 진입점이 없으므로 빈 `LaunchDescription`을 반환한다.
