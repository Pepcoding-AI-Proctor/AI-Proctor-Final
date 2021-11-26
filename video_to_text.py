from pydub import AudioSegment 
from pydub.utils import make_chunks 
import os
import speech_recognition as sr
import ffmpeg

import moviepy.editor as mp

def video2audio(videopath,video_folder_path):

    # Python code to convert video to audio
    import moviepy.editor as mp

    # Insert Local Video File Path
    clip = mp.VideoFileClip(videopath)

    # Insert Local Audio File Path
    audiopath = os.path.join(video_folder_path,"audio.wav")
    clip.audio.write_audiofile(audiopath)
    
    
    
def split_audio(video_folder_path):
    chunk_folderpath = os.path.join(video_folder_path,"Audio Chunks")
    try:
        os.mkdir(chunk_folderpath)
    except:
        pass       
        
    audiopath = os.path.join(video_folder_path,"audio.wav")
    myaudio = AudioSegment.from_file(audiopath, "wav")  #
    chunk_length_ms = 30000 # pydub calculates in millisec 
    chunks = make_chunks(myaudio,chunk_length_ms) #Make chunks of one sec 
    for i, chunk in enumerate(chunks): 
        chunk_name = "{0}.wav".format(i) 
        print ("exporting", chunk_name) 
        chunk_path = os.path.join(chunk_folderpath,chunk_name)
        chunk.export(chunk_path, format="wav") 
    
    
def audio2text(video_folder_path,filename = "audio_text.txt"):
    
    chunk_folderpath = os.path.join(video_folder_path,"Audio Chunks")
    text_filepath = os.path.join(video_folder_path,filename)
    open(text_filepath, 'w').close() ##deleting the content of text file if it exists
    
    text = ""
    path = os.walk(chunk_folderpath)
    r = sr.Recognizer()
    for root, dirr, files in path:
        for file in files:
            filepath = os.path.join(chunk_folderpath,file)
            with sr.AudioFile(filepath) as source:
                audio = r.record(source) 
            try:
                text = r.recognize_google(audio,language = 'en-IN')
                
            except:
                text = "No audio found"
    
            with open(text_filepath,'a') as f:
                
                f.write(text)
                f.write("\n")
        
        
def video_to_text(videopath,video_folder_path):
    
    video2audio(videopath,video_folder_path)
    print("Converted the video successfully to audio")
    
    split_audio(video_folder_path)
    print("Successfully Converted the audio to chunks")
    
    audio2text(video_folder_path)
    print("Text file saved successfully")

    
    
    