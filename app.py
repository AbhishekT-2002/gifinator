import os
import subprocess
from pathlib import Path
from pytube import YouTube
import moviepy.editor as mp
import whisper
from whisper.utils import get_writer
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.VideoClip import TextClip
from moviepy.config import change_settings
#Set ImageMagick binary path
change_settings({"IMAGEMAGICK_BINARY": "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

def get_video_source():
    while True:
        source = input("Enter YouTube URL or local file path: ")
        if source.startswith("http"):
            return source, "youtube"
        elif os.path.exists(source):
            return source, "local"
        else:
            print("Invalid input. Please enter a valid YouTube URL or local file path.")

def get_video_portion():
    while True:
        choice = input("1. Use entire video\n2. Use a part of the video\nEnter your choice (1 or 2): ")
        if choice == "1":
            return None
        elif choice == "2":
            start = input("Enter start time (HH:MM:SS): ")
            end = input("Enter end time (HH:MM:SS): ")
            if validate_time_format(start) and validate_time_format(end):
                duration = calculate_duration(start, end)
                if duration <= 7:
                    return start, end
                else:
                    print("Duration exceeds 7 seconds. Please try again.")
            else:
                print("Invalid time format. Please use HH:MM:SS.")
        else:
            print("Invalid choice. Please enter 1 or 2.")

def validate_time_format(time_str):
    try:
        hours, minutes, seconds = map(int, time_str.split(':'))
        return 0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60
    except:
        return False

def calculate_duration(start, end):
    start_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(start.split(':'))))
    end_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(end.split(':'))))
    return end_seconds - start_seconds

def get_project_name():
    while True:
        name = input("Enter project name: ")
        if os.path.exists(name):
            print("Project already exists. Please use a different name.")
        else:
            return name

def download_youtube_video(url, output_path):
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    stream.download(output_path=output_path, filename='video.mp4')
    return os.path.join(output_path, 'video.mp4')

def process_video(video_path, project_folder, portion=None):
    video = mp.VideoFileClip(video_path)
    
    if portion:
        video = video.subclip(portion[0], portion[1])
    
    audio_path = os.path.join(project_folder, "audio.wav")
    video.audio.write_audiofile(audio_path)
    
    # Generate subtitles
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    
    srt_path = os.path.join(project_folder, "audio.srt")
    srt_writer = get_writer("srt", project_folder)
    srt_writer(result, audio_path)
    
    # Burn subtitles onto video
    video_generator = lambda txt: TextClip(txt, font='Arial', fontsize=50, color='white', stroke_color='black', stroke_width=1, method='caption', size=(video.w, None))
    video_subtitles = SubtitlesClip(srt_path, video_generator)
    final_video = mp.CompositeVideoClip([video, video_subtitles.set_position(('center', 'bottom'))])
    
    output_video_path = os.path.join(project_folder, "output_video.mp4")
    final_video.write_videofile(output_video_path)
    
    # Create GIF with meme-style text
    gif_generator = lambda txt: TextClip(txt, font='Impact', fontsize=40, color='white', stroke_color='black', stroke_width=2, method='caption', size=(video.w, None))
    gif_subtitles = SubtitlesClip(srt_path, gif_generator)
    gif_video = mp.CompositeVideoClip([video, gif_subtitles.set_position(('center', 'bottom'))])
    
    gif_folder = os.path.join(project_folder, "gifs")
    os.makedirs(gif_folder, exist_ok=True)
    gif_path = os.path.join(gif_folder, "output.gif")
    gif_video.write_gif(gif_path)
    
    video.close()
    final_video.close()
    gif_video.close()

def main():
    video_source, source_type = get_video_source()
    portion = get_video_portion()
    project_name = get_project_name()
    
    os.makedirs(project_name, exist_ok=True)
    
    if source_type == "youtube":
        video_path = download_youtube_video(video_source, project_name)
    else:
        video_path = video_source
    
    process_video(video_path, project_name, portion)
    
    print(f"Processing complete. Output files are in the '{project_name}' folder.")

if __name__ == "__main__":
    main()