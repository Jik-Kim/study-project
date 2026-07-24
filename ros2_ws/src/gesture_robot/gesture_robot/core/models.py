"""노드 내부에서 사용할 Python 데이터 모델 정의 영역."""

from dataclasses import dataclass


@dataclass
class TrackingResult:
    """객체 추적 알고리즘의 처리 결과를 담는 데이터 모델.

    Attributes:
        detected: 객체 검출 여부 (최소 면적 threshold 만족 시 True)
        error_x: 화면 중심 기준 공의 가로 위치 오차 (오른쪽 > 0, 왼쪽 < 0)
        error_y: 화면 중심 기준 공의 세로 위치 오차 (아래쪽 > 0, 위쪽 < 0)
        area: 검출된 공의 픽셀 면적 (거리 근사치)
    """

    detected: bool = False
    error_x: float = 0.0
    error_y: float = 0.0
    area: float = 0.0

