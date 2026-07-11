"""OpenCV 기반 추적 결과 시각화 영역."""

from typing import Any


class TrackingVisualizer:
    """원본 영상 위에 추적 결과와 상태를 표시한다."""

    def render(self, frame: Any, tracking_result: Any) -> None:
        """영상 위에 객체 위치와 디버깅 정보를 그린다."""
        # TODO: 바운딩 박스, 중심점, 상태, FPS 표시를 구현한다.
        raise NotImplementedError
