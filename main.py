import cv2
import mediapipe as mp

print("Program Started...")

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not opening ❌")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(rgb)

if result.pose_landmarks:
    landmarks = result.pose_landmarks.landmark

    left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y
    right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y
    nose = landmarks[mp_pose.PoseLandmark.NOSE].y

    # Simple rule-based detection
    if left_wrist < nose and right_wrist < nose:
        cv2.putText(frame, "Suspicious Activity Detected!", 
                    (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0, 0, 255), 2)
        mp_drawing.draw_landmarks(
            frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS
        )

    cv2.imshow("AI Surveillance", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()