import cv2
import mediapipe as mp
import numpy as np
import math

def calculate_angle(a, b, c):
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

def run_posture_detection():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    # Get screen resolution
    screen_width = 1920  # Default screen width
    screen_height = 1080  # Default screen height
    window_width = int(screen_width * 0.8)  # 80% of screen width
    window_height = int(screen_height * 0.8)  # 80% of screen height
    
    # Create named window and set its position
    cv2.namedWindow("Posture Detector", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Posture Detector", window_width, window_height)
    window_x = (screen_width - window_width) // 2
    window_y = (screen_height - window_height) // 2
    cv2.moveWindow("Posture Detector", window_x, window_y)

    def calculate_posture(landmarks, image):
        left_shoulder = landmarks.landmark[11]
        right_shoulder = landmarks.landmark[12]
        left_hip = landmarks.landmark[23]
        right_hip = landmarks.landmark[24]

        image_height, image_width, _ = image.shape
        l_shldr_y = left_shoulder.y * image_height
        r_shldr_y = right_shoulder.y * image_height
        l_hip_y = left_hip.y * image_height
        r_hip_y = right_hip.y * image_height

        shoulder_diff = abs(l_shldr_y - r_shldr_y)
        hip_diff = abs(l_hip_y - r_hip_y)

        if shoulder_diff > 20 or hip_diff > 20:
            return "Bad Posture"
        else:
            return "Good Posture"

    def draw_angle_panel(image, angles):
        panel_width = 300
        panel_start_x = image.shape[1] - panel_width
        
        # Create semi-transparent overlay for the panel
        overlay = image.copy()
        cv2.rectangle(overlay, (panel_start_x, 0), (image.shape[1], image.shape[0]), 
                     (33, 33, 33), -1)
        
        # Apply transparency
        alpha = 0.85
        image = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)
        
        # Draw panel title
        cv2.putText(image, "Joint Angles", (panel_start_x + 20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Draw separator line
        cv2.line(image, (panel_start_x + 20, 60), (image.shape[1] - 20, 60),
                (200, 200, 200), 1)
        
        # Draw angles with modern styling
        y_offset = 100
        for name, angle in angles.items():
            # Draw angle name
            cv2.putText(image, name, (panel_start_x + 20, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
            
            # Draw angle value with degree symbol
            angle_text = f"{angle:.1f}°"
            cv2.putText(image, angle_text, (panel_start_x + 20, y_offset + 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            
            # Draw mini separator
            cv2.line(image, (panel_start_x + 20, y_offset + 50),
                    (image.shape[1] - 20, y_offset + 50), (100, 100, 100), 1)
            
            y_offset += 80
            
        return image

    with mp_pose.Pose(min_detection_confidence=0.5,
                      min_tracking_confidence=0.5) as pose:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            
            # Create black background
            background = np.zeros((window_height, window_width, 3), dtype=np.uint8)
            
            # Resize frame to fit in window while maintaining aspect ratio
            frame_height, frame_width = frame.shape[:2]
            aspect_ratio = frame_width / frame_height
            
            if window_width / window_height > aspect_ratio:
                new_width = int(window_height * aspect_ratio)
                new_height = window_height
            else:
                new_width = window_width
                new_height = int(window_width / aspect_ratio)
                
            frame_resized = cv2.resize(frame, (new_width, new_height))
            
            # Calculate position to center the frame
            y_offset = (window_height - new_height) // 2
            x_offset = (window_width - new_width) // 2
            
            # Place the frame in the center of the background
            background[y_offset:y_offset+new_height, x_offset:x_offset+new_width] = frame_resized
            
            image = cv2.cvtColor(background, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                # Draw pose landmarks
                mp_drawing.draw_landmarks(
                    image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                # Calculate angles
                landmarks = results.pose_landmarks.landmark
                
                # Calculate key angles
                angles = {
                    "Neck Tilt": calculate_angle(
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                        landmarks[mp_pose.PoseLandmark.NOSE.value],
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
                    ),
                    "Right Shoulder": calculate_angle(
                        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                        landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
                    ),
                    "Left Shoulder": calculate_angle(
                        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
                    ),
                    "Back Angle": calculate_angle(
                        landmarks[mp_pose.PoseLandmark.NOSE.value],
                        landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                        landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
                    ),
                    "Hip Angle": calculate_angle(
                        landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                        landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
                    )
                }
                
                # Draw angle panel
                image = draw_angle_panel(image, angles)

                # Draw posture status
                posture = calculate_posture(results.pose_landmarks, image)
                text_size = cv2.getTextSize(posture, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)[0]
                text_x = (window_width - text_size[0]) // 2
                cv2.putText(image, posture, (text_x, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                            (0, 255, 0) if posture == "Good Posture" else (0, 0, 255), 3)

            cv2.imshow("Posture Detector", image)

            if cv2.waitKey(10) & 0xFF == ord('q') or cv2.waitKey(10) & 0xFF == ord('Q'):
                break

    cap.release()
    cv2.destroyAllWindows()
