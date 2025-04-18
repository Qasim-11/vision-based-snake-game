import cv2
import numpy as np
import mediapipe as mp
import hand
import time
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow INFO and WARNING messages. It actually didn't work :)
def __main__():
    print("Starting snake game")

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.8)
    mp_draw = mp.solutions.drawing_utils

    canvas = None
    frame_width, frame_height = 640, 480  
    snake_length = 5  # Snake tail length
    snake_points = [(frame_width // 2, frame_height // 2)] * snake_length  # Start snake in the center
    snake_speed = 3  

    apple_x = None
    apple_y = None
    
    head_x = frame_width // 2
    head_y = frame_height // 2

    start_time = time.time()

    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break
        frame = cv2.flip(frame, 1)

        # Detect hand
        frame, index_tip_coords, finger_state, hand_detected = hand.getHand(frame, hands, mp_draw, mp_hands.HAND_CONNECTIONS, return_details=True)

        if canvas is None:
            canvas = np.zeros_like(frame)

        if hand_detected and index_tip_coords:
            diff_x = index_tip_coords[0] - snake_points[-1][0]
            diff_y = index_tip_coords[1] - snake_points[-1][1]

            distance = np.sqrt(diff_x**2 + diff_y**2)
            if distance > snake_speed:
                scale = snake_speed / distance
                diff_x = int(diff_x * scale)
                diff_y = int(diff_y * scale)

            head_x = snake_points[-1][0] + diff_x
            head_y = snake_points[-1][1] + diff_y

            # Boundary check
            head_x = max(0, min(frame_width - 1, head_x))
            head_y = max(0, min(frame_height - 1, head_y))

            new_head = (head_x, head_y)

            snake_points.append(new_head)
            if len(snake_points) > snake_length:
                snake_points.pop(0)
        else:
            # If the hand is not detected, the snake keeps moving in the last direction
            if len(snake_points) > 1:
                last_diff_x = snake_points[-1][0] - snake_points[-2][0]
                last_diff_y = snake_points[-1][1] - snake_points[-2][1]
                new_head = (
                    snake_points[-1][0] + last_diff_x,
                    snake_points[-1][1] + last_diff_y,
                )

                # Boundary check
                new_head = (
                    max(0, min(frame_width - 1, new_head[0])),
                    max(0, min(frame_height - 1, new_head[1])),
                )

                snake_points.append(new_head)
                if len(snake_points) > snake_length:
                    snake_points.pop(0)

        canvas = np.zeros_like(frame)  
        for i in range(1, len(snake_points)):
            cv2.line(canvas, snake_points[i - 1], snake_points[i], (0, 255, 0), 7)  # Red snake body
        cv2.circle(canvas, snake_points[-1], 10, (0, 240, 0), -1)  # Green snake head

        combined = cv2.addWeighted(frame, 0.6, canvas, 1, 0)

        # Randomly generate an apple
        apple_x = np.random.randint(140, frame_width - 140) if apple_x is None else apple_x
        apple_y = np.random.randint(60, frame_height - 60) if apple_y is None else apple_y
        cv2.circle(combined, (apple_x, apple_y), 10, (0, 0, 255), -1)

        # Check if the snake has eaten the apple
        if np.sqrt((snake_points[-1][0] - apple_x)**2 + (snake_points[-1][1] - apple_y)**2) < 10:
            snake_length += 5
            snake_speed += 1

            apple_x = None 
            apple_y = None
            
        # if the snake hits itself, break
        if time.time() - start_time > 20:
            print("Losing time")
            for point in snake_points[:-2]:  # don't change -2, because -1 is the head
                # print((snake_points[-1][0] - point[0])**2 + (snake_points[-1][1] - point[1])**2)
                if (snake_points[-1][0] - point[0])**2 + (snake_points[-1][1] - point[1])**2 <= 8:  # 10^2 = 100
                    print("Game Over: You hit yourself")
                    cap.release()
                    cv2.destroyAllWindows()
                    print("Your score is: ", snake_length - 5)
                    return


            # if the snake hits the wall, break 
            if snake_points[-1][0] <= 10 or snake_points[-1][0] >= frame_width - 10 or snake_points[-1][1] <= 10 or snake_points[-1][1] >= frame_height -10:
                print("Game Over, you hit the wall")
                print("Your score is: ", snake_length - 5)
                return
        cv2.putText(combined, f"Score {snake_length - 5}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(combined, f"Best Score : 70" , (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 215, 255), 2) # if you want a gold coloring for the best score, change the color to (0, 215, 255)
        cv2.imshow("Snake Game", combined)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    __main__()
