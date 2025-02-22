from openai import OpenAI
import os

def audio_to_text(audio_file_path):
    import whisper

    # Load the Whisper model
    model = whisper.load_model("tiny")

    # Transcribe the audio file
    result = model.transcribe(audio_file_path)

    # Extract the text from the transcription
    text = result["text"]

    text_name = os.path.splitext(os.path.basename(audio_file_path))[0]
    dir_name = os.path.dirname(audio_file_path)
    text_file_path = os.path.join(dir_name,text_name+'.txt')

    # Write the text to the specified file
    with open(text_file_path, "w") as text_file:
        text_file.write(text)
    
    return text_file_path

