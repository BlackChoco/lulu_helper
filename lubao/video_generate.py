import cv2
import numpy as np
import os
import time
import random
import gradio as gr
from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageClip
from io import StringIO
from knowledge_generate import extract_and_summarize

# 将时间字符串转换为秒数
def time_to_seconds(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

# 获取预览视频的开始和结束时间
def get_preview_times(input_video_path, preview_duration=5):
    clip = VideoFileClip(input_video_path)
    video_duration = clip.duration
    clip.close()
    preview_start_seconds = random.randint(0, int(video_duration - preview_duration))
    preview_end_seconds = preview_start_seconds + preview_duration
    preview_start_time = time.strftime('%H:%M:%S', time.gmtime(preview_start_seconds))
    preview_end_time = time.strftime('%H:%M:%S', time.gmtime(preview_end_seconds))
    return preview_start_time, preview_end_time

# 截断视频
def cut_video(input_video_path, output_video_path, start_time=None, end_time=None):
    clip = VideoFileClip(input_video_path)
    start_frame = int(time_to_seconds(start_time) * clip.fps) if start_time else 0
    end_frame = int(time_to_seconds(end_time) * clip.fps) if end_time else int(clip.reader.nframes)

    # 获取视频扩展名
    video_name = os.path.basename(input_video_path)
    
    # 在output_video_path中构建一个video_name的文件夹
    video_name_without_ext = os.path.splitext(video_name)[0]

    output_video_path = os.path.join(output_video_path, video_name_without_ext)
    if not os.path.exists(output_video_path):
        os.makedirs(output_video_path)

    original_clip_path = os.path.join(output_video_path,video_name)
    original_clip = clip.subclip(start_frame / clip.fps, end_frame / clip.fps)
    original_clip.write_videofile(original_clip_path, codec="libx264", audio_codec="aac")
    original_clip.close()
    
    return original_clip_path,"视频截取成功！"

# 处理视频，应用遮挡效果
def process_video(input_video_path, cover_height_ratio=0.15, cover_width_ratio=1.0):
    clip = VideoFileClip(input_video_path)
    def process_frame(frame):
        frame = frame.copy()  # Make a copy of the frame to avoid modifying the read-only array
        height, width = frame.shape[:2]
        cover_height = int(cover_height_ratio * height)
        cover_width = int(cover_width_ratio * width)
        x_start = (width - cover_width) // 2
        y_start = height - cover_height

        # 创建一个黑色遮挡
        overlay = frame.copy()
        alpha = 1
        cover_color = (0, 0, 0)  # 黑色遮挡
        cv2.rectangle(overlay, (x_start, y_start), (x_start + cover_width, y_start + cover_height), cover_color, -1)
        frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

        # 添加边框
        border_color = (255, 255, 255)  # 白色边框
        border_thickness = 2
        cv2.rectangle(frame, (x_start, y_start), (x_start + cover_width, y_start + cover_height), border_color, border_thickness)
        return frame

    dir_name = os.path.dirname(input_video_path)
    video_name = os.path.basename(input_video_path)
    output_video_path = os.path.join(dir_name,"mosaic_"+ video_name)

    new_clip = clip.fl_image(process_frame)
    new_clip.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
    new_clip.close()
    
    return output_video_path


# 拼接两个视频
def concatenate_videos(mosaic_video_path,raw_video_path,  pic1_path, pic2_path):
    # 获取视频高度
    video_height = VideoFileClip(mosaic_video_path).h
    
    # 创建图片片段并调整大小以匹配视频高度
    pic1_clip = ImageClip(pic1_path).set_duration(2).resize(height=video_height)
    pic2_clip = ImageClip(pic2_path).set_duration(2).resize(height=video_height)
    
    # 创建视频片段
    clip1 = VideoFileClip(mosaic_video_path)
    clip2 = VideoFileClip(raw_video_path)
    
    # 拼接片段
    final_clip = concatenate_videoclips([pic1_clip, clip1, pic2_clip, clip2], method="compose")
    
    dir_name = os.path.dirname(raw_video_path)
    video_name = os.path.basename(raw_video_path)
    output_path = os.path.join(dir_name,"concatnated_"+ video_name)

    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    
    # 关闭片段
    pic1_clip.close()
    pic2_clip.close()
    clip1.close()
    clip2.close()
    final_clip.close()

    return output_path

def video_process_concatnate(input_video_path,cover_height_ratio_value=0.15, cover_width_ratio_value=1, pic1_path_value='utils/pic/pic1.png', pic2_path_value='utils/pic/pic2.png'):

    mosaic_video_path = process_video(input_video_path,cover_height_ratio=cover_height_ratio_value,cover_width_ratio=cover_width_ratio_value)
    concatenate_video_path = concatenate_videos(mosaic_video_path,input_video_path,pic1_path=pic1_path_value, pic2_path=pic2_path_value)
    
    return concatenate_video_path
