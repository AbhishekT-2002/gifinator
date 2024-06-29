# Gifinator - Captioned GIFs from Videos

This project helps you create captioned GIFs from YouTube videos or local video files using Python. The GIFs will feature large white captions at the bottom of each GIF.

## Prerequisites

- Python 3.7 or higher
- FFmpeg
- ImageMagick

## Setup

1. **Clone the repository:**
    ```sh
    git clone https://github.com/AbhishekT-2002/gifinator
    cd gifinator
    ```

2. **Install required Python libraries:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Install FFmpeg:**
    - Follow the instructions on the [FFmpeg website](https://ffmpeg.org/download.html).

4. **Install ImageMagick:**
    - Follow the instructions on the [ImageMagick website](https://imagemagick.org/script/download.php).
    - Set the ImageMagick binary path in the `moviepy` configuration as shown in the script.

5. **Install OpenAI Whisper:**
    - Check out the [OpenAI Whisper GitHub page](https://github.com/openai/whisper) for installation instructions and more details.

## Usage

1. **Run the script:**
    ```sh
    python app.py
    ```

2. **Follow the prompts:**
    - Enter the YouTube URL or local file path of the video.
    - Choose whether to use the entire video or a part of it. If choosing a part, provide the start and end times in `HH:MM:SS` format.
    - Enter a project name. If a project with the same name exists, you will be prompted to choose a different name.

3. **Processing:**
    - The script will download the video if it is from YouTube.
    - The script will separate the audio from the video.
    - OpenAI Whisper will transcribe the audio and generate an `.srt` file.
    - The script will burn the subtitles onto the video and save it as an output video file.
    - The script will create a GIF with the subtitles and save it in a `gifs` folder inside the project folder.

4. **Output:**
    - The processed video and GIF files will be saved in the specified project folder.

## Example

Here is an example of how to run the script and its expected prompts:

```sh
$ python script.py
Enter YouTube URL or local file path: https://www.youtube.com/watch?v=dQw4w9WgXcQ
1. Use entire video
2. Use a part of the video
Enter your choice (1 or 2): 2
Enter start time (HH:MM:SS): 00:01:00
Enter end time (HH:MM:07): 00:01:07
Enter project name: my_video_project
Processing complete. Output files are in the 'my_video_project' folder.
