'''
Run the below commands in terminal

pip install mtcnn
pip install keras_vggface keras_applications

Make the changes mentioned in the below webpage 
https://stackoverflow.com/a/68964904
'''



from mtcnn.mtcnn import MTCNN
import cv2
import numpy as np
from keras_vggface.utils import preprocess_input
from keras_vggface.vggface import VGGFace
from scipy.spatial.distance import cosine 


## Refer this link to deal with error in above imports
## https://stackoverflow.com/a/68964904


import warnings
warnings.filterwarnings('ignore',category = FutureWarning)


detector =  MTCNN()

#######function to extract face from an image ################
def extract_face(image,resize = (224,224)):

    #image = cv2.imread(image)
    faces = detector.detect_faces(image)
    x1,y1,width,height = faces[0]['box']

    x2,y2,= x1+width,y1+height

    face_boundary = image[y1:y2,x1:x2]

    face_image = cv2.resize(face_boundary,resize)

    return face_image

###########function to extract face from an image filepath #################
def extract_face_from_path(image,resize = (224,224)):
    image = cv2.imread(image)
    faces = detector.detect_faces(image)
    x1,y1,width,height = faces[0]['box']

    x2,y2,= x1+width,y1+height

    face_boundary = image[y1:y2,x1:x2]

    face_image = cv2.resize(face_boundary,resize)

    return face_image

############ function to create a 2048 dimensional embedding of array of faces ##############
def get_embeddings(faces):
    
    face = np.asarray(faces,'float32')
    face = preprocess_input(face,version = 2)

    model = VGGFace(model='resnet50',include_top = False,input_shape=(224,224,3), pooling='avg')

    return model.predict(face)

############ function to find cosine dstance between array of embeddings #################
def get_similarity(faces):

  embeddings = get_embeddings(faces)
  score = cosine(embeddings[0], embeddings[1])

  if score <= 0.5:
    return "face Matched", score
  return "face not matched",score


###### final function to find out whether two faces matches or not ####################

def match_faces(profile_imgpath, current_frame,matching_list):
    try:
        current_face = extract_face(current_frame)
    except:
        matching_list.append("No face Found")
        return
    profile_face = extract_face_from_path(profile_imgpath)
    
    status,similarity = get_similarity([profile_face,current_face])
    
    
    if similarity<=0.5:
        matching_list.append("Face Matched")
        return
    else:
        matching_list.append("Face not Matched")
    
    

