import cv2
import mediapipe as mp
import math
import os
import datetime

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

draw_points = []
color = (0, 0, 255)  # Default RED

# Create save folder
save_path = "saved_drawings"
if not os.path.exists(save_path):
    os.makedirs(save_path)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, c = frame.shape

            lm = hand_landmarks.landmark

            # Get fingertip coordinates
            x2 = int(lm[8].x * w)
            y2 = int(lm[8].y * h)

            # Finger states
            fingers = []

            # Index
            fingers.append(lm[8].y < lm[6].y)
            # Middle
            fingers.append(lm[12].y < lm[10].y)
            # Ring
            fingers.append(lm[16].y < lm[14].y)
            # Pinky
            fingers.append(lm[20].y < lm[18].y)

            total_fingers = fingers.count(True)

            # Color selection
            if total_fingers == 0:
                color = (0, 0, 255)  # RED
            elif total_fingers == 2:
                color = (0, 255, 0)  # GREEN
            elif total_fingers == 3:
                color = (255, 0, 0)  # BLUE

            # Pinky only → erase
            if fingers == [False, False, False, True]:
                draw_points.clear()

            # Pinch detection
            x1 = int(lm[4].x * w)
            y1 = int(lm[4].y * h)
            distance = math.hypot(x2 - x1, y2 - y1)

            if distance < 40:
                draw_points.append((x2, y2, color))
            else:
                draw_points.append(None)

    # Draw lines
    for i in range(1, len(draw_points)):
        if draw_points[i - 1] and draw_points[i]:
            cv2.line(
                frame,
                draw_points[i - 1][:2],
                draw_points[i][:2],
                draw_points[i][2],
                5
            )

    cv2.imshow("AirDraw Advanced", frame)

    key = cv2.waitKey(1)

    # Save image
    if key == ord('s'):
        filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
        cv2.imwrite(os.path.join(save_path, filename), frame)
        print("Saved:", filename)

    # Clear screen
    if key == ord('c'):
        draw_points.clear()

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
