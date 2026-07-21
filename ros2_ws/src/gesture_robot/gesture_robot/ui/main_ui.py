"""Tkinter 기반 메인 UI 영역."""

import tkinter as tk
from tkinter import ttk
from typing import Optional

import cv2
import numpy as np
from PIL import Image, ImageTk


class MainUI:
    _TITLE = "Gesture-Controlled Tracking Robot"
    _WIDTH = 860
    _HEIGHT = 680
    _CAM_W = 640
    _CAM_H = 360
    _SIM_H = 200
    _TICK_MS = 50

    _GESTURE_NAMES = {0: "NONE", 1: "START", 2: "STOP"}

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(self._TITLE)
        self.root.geometry(f"{self._WIDTH}x{self._HEIGHT}")
        self.root.resizable(False, False)

        self._cam_photo: Optional[ImageTk.PhotoImage] = None
        self._sim_photo: Optional[ImageTk.PhotoImage] = None

        self._build_ui()
        self._mock_start()

    # --- Build UI ---

    def _build_ui(self) -> None:
        self._build_camera()
        self._build_status()
        self._build_simulation()

    def _build_camera(self) -> None:
        frame = ttk.LabelFrame(self.root, text="CAMERA", padding=5)
        frame.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        self._cam_canvas = tk.Canvas(
            frame, width=self._CAM_W, height=self._CAM_H,
            bg="black", highlightthickness=0,
        )
        self._cam_canvas.pack()
        self._cam_canvas.create_text(
            self._CAM_W // 2, self._CAM_H // 2,
            text="CAMERA FEED", fill="#444", font=("Arial", 18),
        )

    def _build_status(self) -> None:
        frame = ttk.LabelFrame(self.root, text="STATUS", padding=10)
        frame.pack(fill="x", padx=10, pady=5)

        self._svars: dict[str, tk.StringVar] = {}
        fields = [
            ("Tracking", "tracking"),
            ("Gesture", "gesture"),
            ("Confidence", "confidence"),
            ("Error X", "error_x"),
            ("Error Y", "error_y"),
            ("Area", "area"),
            ("FPS", "fps"),
        ]

        for col, (label, key) in enumerate(fields):
            self._svars[key] = tk.StringVar(value="--")
            ttk.Label(frame, text=label).grid(
                row=0, column=col * 2, sticky="w", padx=(5, 2),
            )
            ttk.Label(frame, textvariable=self._svars[key]).grid(
                row=0, column=col * 2 + 1, sticky="w", padx=(0, 10),
            )

    def _build_simulation(self) -> None:
        frame = ttk.LabelFrame(self.root, text="SIMULATION", padding=5)
        frame.pack(fill="x", padx=10, pady=(5, 10))

        self._sim_canvas = tk.Canvas(
            frame, width=self._CAM_W, height=self._SIM_H,
            bg="#f0f0f0", highlightthickness=0,
        )
        self._sim_canvas.pack()
        self._sim_canvas.create_text(
            self._CAM_W // 2, self._SIM_H // 2,
            text="TURTLESIM", fill="#ccc", font=("Arial", 20),
        )

    # --- Public API (2단계에서 ROS2 Subscribe 시 호출) ---

    def update_camera_frame(self, frame: np.ndarray) -> None:
        """OpenCV BGR 프레임을 CAMERA 영역에 표시한다."""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)
        pil_img = pil_img.resize((self._CAM_W, self._CAM_H), Image.LANCZOS)
        self._cam_photo = ImageTk.PhotoImage(pil_img)
        self._cam_canvas.delete("all")
        self._cam_canvas.create_image(
            self._CAM_W // 2, self._CAM_H // 2,
            image=self._cam_photo,
        )

    def update_status(
        self,
        tracking: str,
        gesture: int,
        confidence: float,
        error_x: float,
        error_y: float,
        area: float,
        fps: float,
    ) -> None:
        """모니터링 상태 정보를 갱신한다."""
        self._svars["tracking"].set(tracking)
        self._svars["gesture"].set(
            self._GESTURE_NAMES.get(gesture, f"UNKNOWN({gesture})"),
        )
        self._svars["confidence"].set(f"{confidence:.2f}")
        self._svars["error_x"].set(f"{error_x:+.1f}")
        self._svars["error_y"].set(f"{error_y:+.1f}")
        self._svars["area"].set(f"{area:.0f}")
        self._svars["fps"].set(f"{fps:.1f}")

    # --- Standalone mock (이번 주 테스트용, 2단계에서 제거) ---

    def _mock_start(self) -> None:
        self._mock_t = 0
        self._tick()

    def _tick(self) -> None:
        self._mock_t = (self._mock_t + 1) % 150

        t = self._mock_t
        if t < 50:
            tracking, gesture, conf, ex, ey, area, fps = (
                "STOP", 0, 0.0, 0.0, 0.0, 0.0, 30.0
            )
        elif t < 100:
            tracking, gesture, conf, ex, ey, area, fps = (
                "START", 1, 0.95, 42.0, -18.0, 1234.0, 30.0
            )
        else:
            tracking, gesture, conf, ex, ey, area, fps = (
                "STOP", 2, 0.88, 0.0, 0.0, 0.0, 30.0
            )

        self.update_status(tracking, gesture, conf, ex, ey, area, fps)
        self.root.after(self._TICK_MS, self._tick)

    # --- Run ---

    def run(self) -> None:
        """UI 애플리케이션을 실행한다."""
        self.root.mainloop()


def main() -> None:
    app = MainUI()
    app.run()


if __name__ == "__main__":
    main()
