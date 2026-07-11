"""객체 위치를 로봇 이동 명령으로 변환하는 제어 영역."""

from typing import Any


class TrackingController:
    """추적 상태와 객체 위치로 이동 명령을 계산한다."""

    def calculate(self, tracking_state: Any, tracking_result: Any) -> Any:
        """현재 입력에 대응하는 로봇 이동 명령을 반환한다."""
        # TODO: 단순 비례 제어를 먼저 구현하고 필요할 때 PID로 확장한다.
        pass
