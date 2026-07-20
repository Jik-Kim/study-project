"""OpenCV 카메라 입력 연결 영역."""

from typing import Any


class OpenCVCamera:
    """카메라 장치로부터 영상 프레임을 제공한다."""

    def open(self) -> None:
        """카메라 장치를 연다."""
        # TODO: 카메라 번호와 해상도를 파라미터로 받아 연결한다.
        pass

    def read(self) -> Any:
        """카메라에서 한 프레임을 읽는다."""
        # TODO: 프레임 읽기와 실패 처리를 구현한다.
        pass

    def release(self) -> None:
        """카메라 자원을 해제한다."""
        # TODO: OpenCV 카메라 자원 해제를 구현한다.
        pass
