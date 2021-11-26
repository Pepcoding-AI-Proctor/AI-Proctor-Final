import torch

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5m')  # yolov5s or yolov5m, yolov5l, yolov5x, custom

def detect_objects(frame,object_list):
    objects = dict()
    results = model(frame)
    
    items = list(results.pandas().xyxy[0]['name'])
    
    object_list.append(items)
    
    