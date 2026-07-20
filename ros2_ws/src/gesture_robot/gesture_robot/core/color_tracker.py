"""HSV 기반 색상 객체 추적 알고리즘 영역."""

from typing import Any


class ColorTracker:
    """영상 프레임에서 지정한 색상 객체를 추적한다."""

    def track(self, frame: Any) -> Any:
        """객체의 검출 여부, 중심 오차, 면적을 반환한다."""
        # TODO: HSV 변환, 마스크 생성, 노이즈 제거, 윤곽선 검출을 구현한다.
        pass
