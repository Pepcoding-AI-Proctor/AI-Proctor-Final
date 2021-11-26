import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
import math
THRESHOLD = 0.015

pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def get_shoulder_points(frame):
     # Recolor image to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Make detection
    results = pose.process(image)
    
    if results.pose_landmarks == None:
        return False,"No Shoulders Found"
    
    keypoints = []
    for data_point in results.pose_landmarks.landmark:
        keypoints.append({
                             'X': data_point.x,
                             'Y': data_point.y,
                             'Z': data_point.z,
                             'Visibility': data_point.visibility,
                             })
        
    p1 = (keypoints[11]['X'], keypoints[11]['Y'])
    p2 = (keypoints[12]['X'], keypoints[12]['Y'])
    
    return (p1,p2)

def detect_shoulder_movement(old_frame,current_frame,sm_list,threshold = 0.015):
    
    op1,op2 = get_shoulder_points(current_frame)
    np1,np2 = get_shoulder_points(current_frame)
    
    if op1 == False:
        sm_list.append("No Shoulders Found in previous Frame")
        return
    if np1 == False:
        sm_list.append("No Shoulders Found in current Frame")
        return 
    
    pd1 = euclidean_distance(np1, op1)
    pd2 = euclidean_distance(np2, op2)
    
    pda = (pd1 + pd2)/2
    
    if pda > threshold:
        sm_list.append("Moving")
        return 
    else:
        sm_list.append("Stable")
        return 
    
    
    
    
    
    
