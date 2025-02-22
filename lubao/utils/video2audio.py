import moviepy.editor as mp
import os

def extract_audio_from_video(video_path):
    video = mp.VideoFileClip(video_path)
    audio = video.audio

    audio_name = os.path.splitext(os.path.basename(video_path))[0]
    dir_name = os.path.dirname(video_path)

    audio_output_path = os.path.join(os.path.join(dir_name ,audio_name)+'.wav')
    
    if audio is not None:
        audio.write_audiofile(audio_output_path)
    else:
        print("Error: No audio found in the video file.")
    
    return audio_output_path
