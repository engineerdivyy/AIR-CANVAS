import cv2
import mediapipe as mp
import numpy as np
import math

# ================= INIT =================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

canvas = None

# Default Color & Thickness
draw_color = (255, 0, 0) # Blue default
brush_thickness = 10
eraser_thickness = 50
prev_x, prev_y = 0, 0

# ================= UTILS =================
def dist(p1, p2):
    return math.hypot(p1[0]-p2[0], p1[1]-p2[1])

# ================= MAIN LOOP =================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # ⚠️ CANVAS SETUP
    if canvas is None or canvas.shape[:2] != (h, w):
        canvas = np.zeros((h, w, 3), dtype=np.uint8)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    # -------- 1. TOP COLOR BAR UI --------
    cv2.rectangle(frame, (0,0), (w, 100), (40,40,40), -1) # Header bg

    # Color Buttons
    color_boxes = [
        ((50, 20, 140, 80), (255, 0, 0)),   # Blue
        ((160, 20, 250, 80), (0, 255, 0)),  # Green
        ((270, 20, 360, 80), (0, 0, 255)),  # Red
        ((380, 20, 470, 80), (0, 255, 255)),# Yellow
        ((490, 20, 600, 80), (0, 0, 0))     # Eraser
    ]

    for box, col in color_boxes:
        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), col, -1)
        # Highlight Selected in Top Menu
        if draw_color == col:
             cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (255,255,255), 3)

    cv2.putText(frame, "CLEAR", (505, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)


    # -------- 2. SIDEBAR STATUS (NEW FEATURE) --------
    # Right side mein ek box jo current color dikhayega
    
    # Label Text
    cv2.putText(frame, "Selected:", (1120, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Status Box (White Border)
    cv2.rectangle(frame, (1120, 140), (1240, 260), (255, 255, 255), 3)
    
    # Status Box (Fill with Current Color)
    cv2.rectangle(frame, (1120, 140), (1240, 260), draw_color, -1)

    # Agar Eraser (Black) hai to text likho, warna color dikhao
    if draw_color == (0, 0, 0):
        cv2.putText(frame, "Eraser", (1140, 210), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.7, (255, 255, 255), 2)


    # -------- 3. HAND TRACKING LOGIC --------
    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            lm = hand.landmark

            ix, iy = int(lm[8].x*w), int(lm[8].y*h)   # Index Tip
            tx, ty = int(lm[4].x*w), int(lm[4].y*h)   # Thumb Tip

            # 🎨 COLOR SELECTION (Top Area)
            if iy < 100:
                for box, col in color_boxes:
                    if box[0] < ix < box[2]:
                        draw_color = col
                        prev_x, prev_y = 0, 0

            # ✍️ DRAWING (Canvas Area)
            elif dist((ix,iy),(tx,ty)) < 40:
                if prev_x == 0:
                    prev_x, prev_y = ix, iy
                
                thickness = eraser_thickness if draw_color==(0,0,0) else brush_thickness
                
                cv2.line(canvas, (prev_x, prev_y), (ix, iy), draw_color, thickness)
                prev_x, prev_y = ix, iy
            
            else:
                prev_x, prev_y = 0, 0

            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    # -------- 4. MERGE LAYERS --------
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    frame_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
    canvas_fg = cv2.bitwise_and(canvas, canvas, mask=mask)
    frame = cv2.add(frame_bg, canvas_fg)

    cv2.putText(frame, "Press 'c' to Clear Canvas", (10, h-20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200,200,200), 2)

    cv2.imshow("Air Canvas Pro", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('c'):
        canvas = np.zeros((h, w, 3), dtype=np.uint8)

cap.release()
cv2.destroyAllWindows()