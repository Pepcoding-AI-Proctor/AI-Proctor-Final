from head_position import head_position
from object_detection import detect_objects
from liveliness_detector import detect_liveliness
from face_matching import match_faces
from eye_movement import track_movement
from shoulder_movement import detect_shoulder_movement


import cv2
import threading
import time
import pandas as pd
import numpy as np
import os


#######function to get frame rate of video from path in fps
def get_frame_rate(videopath):
    cap = cv2.VideoCapture(videopath)
    fps = int(cap.get(cv2. CAP_PROP_FPS))
    
    return fps


#########function to get total frames in a video from path
def get_total_frames(videopath):
    cap = cv2.VideoCapture(videopath)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    return length




######### fnction to get random frames 
def generate_simulations(total_frames,rate):
    frames = []
    
    start = 1
    end = start + rate
    
    while end < total_frames:
        rn = np.random.randint(start,end)
        frames.append(rn)
        
        start += rate
        end += rate
        
    return frames

'''
User Inputs 
1. videopath
2. path to save frames
3. path to save csv out
4. check rate 

'''



def video_analysis(videopath,video_folder_path,check_rate):
    
    frames_path = os.path.join(video_folder_path,"All Frames")
    output_path = os.path.join(video_folder_path,"vid_insights.csv")
    fps = get_frame_rate(videopath)
    
    
    try:
        os.mkdir(frames_path)
    except:
        pass
    
    open(output_path, 'w').close() ##deleting the content of text file if it exists
    
    
    
    fps = get_frame_rate(videopath)
    total_frames = get_total_frames(videopath)
    
    interval = check_rate*fps  ### number of frames for which one frame will be checked at a time
    
    random_frames = generate_simulations(total_frames,interval)
    records = 0


    frames = []
    head_positions = []
    objects_detected = []
    
    liveliness_list = []
    frame_timestamps = []
    eye_movement = []
    shoulder_movement = []
    
    df = pd.DataFrame(columns = ['frame','timestamp','Head Position','Objects','Liveliness','Eye Movement','Shoulder Movement'])
    
    df.to_csv(output_path)
    
    
    
    start = time.time()
    cap = cv2.VideoCapture(videopath)
    frame_count = 0



    while frame_count < total_frames:
        ret,frame = cap.read()
        frame_count += 1
        if frame_count == 1:
            previous_frame = frame

        if frame_count in random_frames:
            frame_timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC))

            frames.append(frame_count)
            duration = round(frame_count / fps,3)
            framepath = os.path.join(frames_path,"Frame_{} duration {}.jpg".format(frame_count,duration))
            cv2.imwrite(framepath,frame)
            records += 1       


            t1 = threading.Thread(target = detect_objects,args = [frame,objects_detected])
            t2 = threading.Thread(target = head_position,args = [frame,head_positions])
            t3 = threading.Thread(target = detect_liveliness,args = [frame,liveliness_list])
            t4 = threading.Thread(target = track_movement,args = [frame,eye_movement])
            t5 = threading.Thread(target = detect_shoulder_movement,args = [previous_frame,frame,shoulder_movement])


            t1.start()
            t2.start()
            t3.start()
            t4.start()
            t5.start()
            

            t1.join()
            t2.join()
            t3.join()
            t4.join()
            t5.join()

            if records%10 == 0:

                mini_df = pd.DataFrame()

                mini_df['frame'] = frames

                frame_timestamps = [round(i/1000,2) for i in frame_timestamps]
                mini_df['timestamp'] = frame_timestamps

              

                mini_df['Head Position'] = head_positions

                mini_df['Objects'] = objects_detected
                
                if len(liveliness_list) < 10:
                    k = 10-len(liveliness_list)
                    for i in range(k):
                        liveliness_list.append(["No Info"])
                        
                if len(shoulder_movement) < 10:
                    k = 10-len(shoulder_movement)
                    for i in range(k):
                        shoulder_movement.append(["No Info"])
                    
                mini_df['Liveliness'] = liveliness_list
                mini_df['Eye Movement'] = eye_movement
                mini_df['Shoulder Movement'] = shoulder_movement

                mini_df.to_csv(output_path,header = False,mode = 'a')

                print("{} records saved".format(records))
                print("Done till {} frames".format(frame_count))
                print("{} seconds elapsed".format(round(time.time() - start,2)))
                print("\n")


                frames = []
                head_positions = []
                objects_detected = []
                
                liveliness_list = []
                frame_timestamps = []
                eye_movement = []
                shoulder_movement = []
        
        
        
        
        
    if records%10 != 0:

        mini_df = pd.DataFrame()

        mini_df['frame'] = frames

        frame_timestamps = [round(i/1000,2) for i in frame_timestamps]
        mini_df['timestamp'] = frame_timestamps


        mini_df['Head Position'] = head_positions

        mini_df['Objects'] = objects_detected

        mini_df['Liveliness'] = liveliness_list
        mini_df['Eye Movement'] = eye_movement
        mini_df['Shoulder Movement'] = shoulder_movement
        
        mini_df.to_csv(output_path,header = False,mode = 'a')

        print("{} records saved".format(records))
        print("Done till {} frames".format(frame_count))
        print("{} seconds elapsed".format(round(time.time() - start,2)))
        print("\n")



    end = time.time()
    print("Task Finished in {} seconds ".format(round(end-start)))
    
    
    
    
    
'''
User Inputs 
1. videopath
2. imgpath
3. path to save frames
4. path to save csv out
5. check rate 
'''
    
    
def face_verification(imgpath,videopath,video_folder_path,check_rate):
    
    frames_path = os.path.join(video_folder_path, "All Frames")
    output_path = os.path.join(video_folder_path, "face_match.csv")
    open(output_path, 'w').close() ##deleting the content of text file if it exists
    try:
        os.mkdir(frames_path)
    except:
        pass
    
    fps = get_frame_rate(videopath)
    total_frames = get_total_frames(videopath)
    
    interval = check_rate*fps  ### number of frames for which one frame will be checked at a time
    
    random_frames = generate_simulations(total_frames,interval)
    records = 0
    
    df = pd.DataFrame(columns = ['frame','timestamp','Face Verification'])
    df.to_csv(output_path)
    
    frames = []
    frame_timestamps = []
    face_info = []
    
    
    start = time.time()
    cap = cv2.VideoCapture(videopath)
    frame_count = 0
    
    while frame_count < total_frames:
        
        ret,frame = cap.read()        
        frame_count += 1
        
        if frame_count in random_frames:
            frame_timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC))

            frames.append(frame_count)
            duration = round(frame_count / fps,3)
            framepath = os.path.join(frames_path,"Frame_{} duration {} .jpg".format(frame_count,duration))
            cv2.imwrite(framepath,frame)
            records += 1   
            
            
            match_faces(imgpath,frame,face_info)
            
            
            if records%10 == 0:

                mini_df = pd.DataFrame()

                mini_df['frame'] = frames

                frame_timestamps = [round(i/1000,2) for i in frame_timestamps]
                mini_df['timestamp'] = frame_timestamps

                mini_df['Face Verification'] = face_info

                mini_df.to_csv(output_path,header = False,mode = 'a')

                print("{} records saved".format(records))
                print("Done till {} frames".format(frame_count))
                print("{} seconds elapsed".format(round(time.time() - start,2)))
                print("\n")


                frames = []
                face_info = []
                frame_timestamps = []
                
            
    
    if records%10 != 0:

        mini_df = pd.DataFrame()

        mini_df['frame'] = frames

        frame_timestamps = [round(i/1000,2) for i in frame_timestamps]
        mini_df['timestamp'] = frame_timestamps

        mini_df['Face Verification'] = face_info

        mini_df.to_csv(output_path,header = False,mode = 'a')

        print("{} records saved".format(records))
        print("Done till {} frames".format(frame_count))
        print("{} seconds elapsed".format(round(time.time() - start,2)))
        print("\n")
        
        
        
        end = time.time()
        print("Task Finished in {} seconds ".format(round(end-start)))
                      
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    