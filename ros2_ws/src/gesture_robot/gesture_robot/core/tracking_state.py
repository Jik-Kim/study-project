"""추적 시작과 정지 상태를 관리하는 영역."""

from typing import Any


class TrackingStateMachine:
    """제스처 명령에 따라 현재 추적 상태를 관리한다."""

    def update(self, gesture_command: Any) -> None:
        """제스처 명령으로 상태를 변경한다."""
        # TODO: 상태 종류와 전이 규칙을 팀 합의 후 구현한다.
        raise NotImplementedError

    def current_state(self) -> Any:
        """현재 추적 상태를 반환한다."""
        # TODO: 초기 상태와 반환 타입을 정의한다.
        raise NotImplementedError
