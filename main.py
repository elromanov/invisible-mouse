import cv2
import mediapipe as mp
from pynput.mouse import Button, Controller
import time

# Initialize MediaPipe Hand model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
mouse = Controller()
mouse_sensitivity = 4500

# Define the connections between landmarks to form lines
connections = [[0, 1], [1, 2], [2, 3], [3, 4], [5, 6], [6, 7], [7, 8], [9, 10], [10, 11], [11, 12],
               [13, 14], [14, 15], [15, 16], [17, 18], [18, 19], [19, 20], [0, 5], [5, 9], [9, 13],
               [13, 17], [0, 17]]

# Open the webcam
capture = cv2.VideoCapture(0)

indexFingerClick = False
middleFingerClick = False
mouse_pos = mouse.position
lastWristPos = (-1, -1)
movement_delay = 0.01

while True:
    # Read frame from the webcam
    ret, frame = capture.read()

    # Flip the frame horizontally for a mirror effect
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB for MediaPipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(frame_rgb)

    # Check if hand landmarks are detected
    if results.multi_hand_landmarks:
        # Loop through each detected hand
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw the landmarks
            for landmark in hand_landmarks.landmark:
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

            # Draw the connections (lines between landmarks)
            for connection in connections:
                x_start = int(hand_landmarks.landmark[connection[0]].x * frame.shape[1])
                y_start = int(hand_landmarks.landmark[connection[0]].y * frame.shape[0])
                x_end = int(hand_landmarks.landmark[connection[1]].x * frame.shape[1])
                y_end = int(hand_landmarks.landmark[connection[1]].y * frame.shape[0])
                cv2.line(frame, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)

        if results.multi_hand_landmarks[0].landmark[8].y < results.multi_hand_landmarks[0].landmark[7].y:
            if(indexFingerClick == False):
                indexFingerClick = True
                print("Index Finger Click")
                mouse.click(Button.left, 1)
        else:
            indexFingerClick = False
        
        if results.multi_hand_landmarks[0].landmark[12].y < results.multi_hand_landmarks[0].landmark[11].y:
            if(middleFingerClick == False):
                middleFingerClick = True
                print("Middle Finger Click")
                mouse.click(Button.right, 1)
        else:
            middleFingerClick = False

        if(lastWristPos[0] != -1 and lastWristPos[1] != -1 and results.multi_hand_landmarks[0].landmark[4].x < results.multi_hand_landmarks[0].landmark[3].x):
            print(lastWristPos[0], results.multi_hand_landmarks[0].landmark[0].x)
            if results.multi_hand_landmarks[0].landmark[0].x != lastWristPos[0] or results.multi_hand_landmarks[0].landmark[0].y != lastWristPos[1]:
                #mouse.position = (results.multi_hand_landmarks[0].landmark[0].x * frame.shape[1], results.multi_hand_landmarks[0].landmark[0].y * frame.shape[0])
                #mouse.position = ((results.multi_hand_landmarks[0].landmark[0].x + lastWristPos[0])*mouse_sensitivity, (results.multi_hand_landmarks[0].landmark[0].y + lastWristPos[1])*mouse_sensitivity)
                
                deltaX = (results.multi_hand_landmarks[0].landmark[0].x - lastWristPos[0]) * mouse_sensitivity
                deltaY = (results.multi_hand_landmarks[0].landmark[0].y - lastWristPos[1]) * mouse_sensitivity

                mouse.move(deltaX, -deltaY)
        lastWristPos = (results.multi_hand_landmarks[0].landmark[0].x, results.multi_hand_landmarks[0].landmark[0].y)
        time.sleep(movement_delay)
    # Display the frame
    cv2.imshow('Hand Detection', frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
capture.release()
cv2.destroyAllWindows()