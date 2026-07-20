"""손 랜드마크를 제스처 명령으로 분류하는 영역."""

from typing import Any


class GestureClassifier:
    """MediaPipe 랜드마크를 프로젝트 명령으로 변환한다."""

    def classify(self, hand_landmarks: Any) -> Any:
        """인식된 손 모양에 대응하는 명령을 반환한다."""
        # TODO: 손 펴기, 주먹, 방향 제스처의 판별 규칙을 구현한다.
        pass
