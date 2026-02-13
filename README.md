# Hand-Tracking

# ✋ Hand Tracking with MediaPipe (Python)

A real-time hand tracking system built using:

- 🎥 OpenCV (camera processing)
- 🖐 MediaPipe (hand landmark detection)
- 🧮 NumPy (math utilities)

This project detects hand landmarks from a webcam feed and enables gesture-based interaction like pinch detection and finger counting.

---

## 🚀 Features

- Real-time webcam hand tracking
- 21 hand landmark detection
- Pinch detection (Thumb + Index)
- Finger counting logic
- Gesture recognition foundation
- Lightweight and fast

---

## 🧠 How It Works

MediaPipe detects 21 3D hand landmarks per frame.

Example important landmarks:

- 0 → Wrist
- 4 → Thumb tip
- 8 → Index tip
- 12 → Middle tip
- 16 → Ring tip
- 20 → Pinky tip

Pinch detection is calculated using the distance between:

Thumb tip (4) and Index tip (8)

If the distance is small → pinch detected.

---

## 🎮 Example Gestures

| Gesture | Detection Logic |
|----------|----------------|
| 🤏 Pinch | Distance(4, 8) < threshold |
| ✊ Fist | No fingers up |
| ✋ Open Palm | 4 fingers up |
| ☝ Index Up | Landmark 8 above landmark 6 |

Finger up detection logic:

```python
tip.y < pip.y
