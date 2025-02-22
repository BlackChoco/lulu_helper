from utils.video2audio import extract_audio_from_video
from utils.audio2text import audio_to_text
from utils.text2knowledge import extract_high_frequency_words_and_expressions

def extract_and_summarize(input_video_path,system_prompt_value):
    audio_path = extract_audio_from_video(input_video_path)
    text_path = audio_to_text(audio_path)
    summary = extract_high_frequency_words_and_expressions(text_path,system_prompt_value)
    return summary





