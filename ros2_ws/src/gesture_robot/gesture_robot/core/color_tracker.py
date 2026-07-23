"""HSV 기반 색상 객체 추적 알고리즘 영역."""

import cv2
import numpy as np


# TODO: OpenCV와 NumPy 사용을 팀에서 확정한 뒤 package.xml과 설치 문서에 의존성을 추가한다.
# TODO: HSV 범위, 최소 검출 면적, 커널 크기를 생성자 인자로 받아 ROS2 파라미터와 연결한다.
# TODO: 공통 인터페이스가 확정되면 dict 대신 내부 추적 결과 모델과 타입 표기를 사용한다.
class ColorTracker:
    """영상 프레임에서 지정한 색상 객체를 추적한다."""

    def __init__(self, min_area: float = 500.0) -> None:
        self.min_area = min_area

        self.lower_red_1 = np.array([0, 100, 100])
        self.upper_red_1 = np.array([10, 255, 255])
        self.lower_red_2 = np.array([170, 100, 100])
        self.upper_red_2 = np.array([179, 255, 255])

    def track(self, frame):
        """객체의 검출 여부, 중심 오차, 면적을 반환한다."""
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask_1 = cv2.inRange(
            hsv_frame,
            self.lower_red_1,
            self.upper_red_1
        )

        mask_2 = cv2.inRange(
            hsv_frame,
            self.lower_red_2,
            self.upper_red_2
        )
        mask = cv2.bitwise_or(mask_1, mask_2)

        kernel = np.ones((5, 5), dtype=np.uint8)

        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_OPEN,
            kernel
        )
        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_CLOSE,
            kernel
        )

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        if not contours:
            return self._not_detected(mask)

        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)

        if area < self.min_area:
            return self._not_detected(mask)

        moments = cv2.moments(largest_contour)
        if moments["m00"] == 0:
            return self._not_detected(mask)

        center_x = int(moments["m10"] / moments["m00"])
        center_y = int(moments["m01"] / moments["m00"])

        frame_height, frame_width = frame.shape[:2]
        frame_center_x = frame_width // 2
        frame_center_y = frame_height // 2

        # TODO: error_y가 양수일 때 화면 아래쪽이라는 부호 규칙을 제어 담당자와 확정한다.
        error_x = center_x - frame_center_x
        error_y = center_y - frame_center_y

        return {
            "detected": True,
            "center_x": center_x,
            "center_y": center_y,
            "error_x": error_x,
            "error_y": error_y,
            "area": area,
            # TODO: 시각화 담당자와 협의해 mask와 contour의 반환 책임을 확정한다.
            "mask": mask,
            "contour": largest_contour,
        }

    @staticmethod
    def _not_detected(mask):
        """객체가 검출되지 않은 결과를 만든다."""
        return {
            "detected": False,
            "center_x": None,
            "center_y": None,
            "error_x": 0,
            "error_y": 0,
            "area": 0.0,
            "mask": mask,
            "contour": None,
        }
