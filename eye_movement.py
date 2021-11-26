import cv2
from gaze_tracking.gaze_tracking import GazeTracking

gaze = GazeTracking()

def track_movement(frame,movement_list):
    
    gaze.refresh(frame)
    
    ll = []
    
    new_frame = gaze.annotated_frame()
    text = ""
    text = ""

#     while(r_true < fps*5):
    if gaze.is_right():
        
        text = "Eye Looking right"
        ll.append(text)
    elif gaze.is_left():
        
        text = "Eye Looking left"
        ll.append(text)
    elif gaze.is_center():
        
        text = "Eye Looking center"
        ll.append(text)
    if gaze.is_upward():
        
        text1 = "Eye Looking Upward"
        ll.append(text1)
    elif gaze.is_downward():
        
        text1 = "Eye Looking Downward"
        ll.append(text1)
    else:
        
        text1 = "Eye Looking Straight"
        ll.append(text1)
        
    movement_list.append(ll)