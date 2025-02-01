import cv2


def getHand(frame, model, drawer, connection_type, draw=True, return_details=True) :
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model.process(imgRGB)  
    index_tip_coords = None
    fingers_state = []
    center = None
    hand_detected = False

    if results.multi_hand_landmarks: 
       hand_detected = True
       for handLms in results.multi_hand_landmarks:
            if draw:
                drawer.draw_landmarks(frame, handLms, connection_type)

                index_tip = handLms.landmark[8]

                # Convert normalized coordinates to pixel coordinates
                h, w, c = frame.shape

                # make a line from the index finter like you're writing
                index_tip_coords = (int(index_tip.x * w), int(index_tip.y * h))
                middle_tip_coords = (int(handLms.landmark[12].x * w), int(handLms.landmark[12].y * h))
                # get the center between the index and middle finger
                center = (int((index_tip_coords[0] + middle_tip_coords[0])) // 2, int((index_tip_coords[1] + middle_tip_coords[1])) // 2)

                            # Other fingers: Compare tip with the middle joint along the y-axis (vertical)

                
                for i in [8, 12, 16, 20]:  # Index, Middle, Ring, Pinky
                    if -(handLms.landmark[i].y) > -(handLms.landmark[i - 2].y):  # Tip above PIP joint
                        fingers_state.append(1)
                    else:
                        fingers_state.append(0)


                
    if return_details:
        return frame, index_tip_coords, fingers_state, hand_detected
    return frame

