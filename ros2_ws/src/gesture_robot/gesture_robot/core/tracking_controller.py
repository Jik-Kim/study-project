"""객체 위치를 로봇 이동 명령으로 변환하는 제어 영역."""

import math
from dataclasses import dataclass


@dataclass
class VelocityCommand:
    """거북이 속도 명령."""
    linear_x: float = 0.0
    angular_z: float = 0.0


class TrackingController:
    """추적 상태와 객체 위치로 이동 명령을 계산한다."""

    def __init__(
        self,
        linear_gain: float = 0.001,
        angular_gain: float = 1.0,
        max_linear_speed: float = 2.0,
        max_angular_speed: float = 2.0,
        min_area_threshold: float = 500.0,
    ) -> None:
        self._linear_gain = linear_gain
        self._angular_gain = angular_gain
        self._max_linear_speed = max_linear_speed
        self._max_angular_speed = max_angular_speed
        self._min_area_threshold = min_area_threshold

    def calculate(
        self,
        tracking_active: bool,
        detected: bool,
        error_x: float,
        error_y: float,
        area: float,
    ) -> VelocityCommand:
        """현재 입력에 대응하는 속도 명령을 반환한다.

        Args:
            tracking_active: 추적 시작 상태 여부 (제스처 START 시 True)
            detected: 객체 검출 여부
            error_x: 화면 중심에서 객체까지의 수평 오차 (양수=우측)
            error_y: 화면 중심에서 객체까지의 수직 오차 (양수=하단)
            area: 검출된 객체의 면적 (px^2)

        Returns:
            VelocityCommand: 선속도(면적 비례), 각속도(위치 각도 비례)
        """
        if not tracking_active or not detected:
            return VelocityCommand(linear_x=0.0, angular_z=0.0)

        linear_x = self._calculate_linear_speed(area)
        angular_z = self._calculate_angular_speed(error_x, error_y)

        return VelocityCommand(
            linear_x=max(-self._max_linear_speed, min(self._max_linear_speed, linear_x)),
            angular_z=max(-self._max_angular_speed, min(self._max_angular_speed, angular_z)),
        )

    def _calculate_linear_speed(self, area: float) -> float:
        """면적에 비례하여 전진 속도를 계산한다."""
        if area < self._min_area_threshold:
            return 0.0
        return self._linear_gain * area

    def _calculate_angular_speed(self, error_x: float, error_y: float) -> float:
        """화면 중심에서 객체까지의 각도로 회전 속도를 계산한다."""
        angle = math.atan2(error_y, error_x)
        return self._angular_gain * angle
