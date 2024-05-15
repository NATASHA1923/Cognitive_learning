import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

# Initialize video capture
cap = cv2.VideoCapture(0)

# Initialize game control variables
game_x = 0
game_y = 0
game_move_speed = 5

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    # Convert the image to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (640, 480))

    # Process the image to detect hands
    results = hands.process(image)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the landmarks of the index finger (landmark id 8)
            index_finger_landmark = hand_landmarks.landmark[8]
            #print(index_finger_landmark)

            # Get the x and y coordinates of the index finger tip
            index_finger_x = index_finger_landmark.x
            index_finger_y = index_finger_landmark.y

            # Calculate the distance between the index finger tip and the center of the screen
            center_x = image.shape[1] // 2
            center_y = image.shape[0] // 2
            distance_to_center_x = center_x - index_finger_x
            distance_to_center_y = center_y - index_finger_y

            # Move the player in the maze based on the distance
            if abs(distance_to_center_x) > abs(distance_to_center_y):
                if distance_to_center_x > 0:
                    game_x -= game_move_speed
                else:
                    game_x += game_move_speed
            else:
                if distance_to_center_y > 0:
                    game_y -= game_move_speed
                else:
                    game_y += game_move_speed

              # Draw the hand landmarks and the game cursor on the image
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            cv2.circle(image, (int(game_x), int(game_y)), 5, (0, 255, 0), -1)       

            # Update the game cursor position
        game_x = game_x + image.shape[1] // 2
        game_y = game_y + image.shape[0] // 2

    # Display the resulting frame
    cv2.imshow('MediaPipe Hand Gesture Recognition', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
hands.close()
cap.release()
cv2.destroyAllWindows()