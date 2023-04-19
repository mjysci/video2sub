import re
import os
import yaml
import ffmpeg
import whisper
import yt_dlp


def get_config():
    """
    Retrieves the user's configuration file if it exists.
    By default, the config file is located in ~/.config/video2txt.yml.
    If the file exists, the function will safely load and return its contents.
    If the file does not exist or there is an error loading it,
    an empty dictionary will be returned.

    Returns:
    dict: The contents of the configuration file, or an empty dictionary if the file
    does not exist or there is an error loading it.
    """
    config_path = os.path.join(
        os.path.expanduser("~"), ".config", "config.video2sub.yml"
    )
    if os.path.exists(config_path):
        with open(config_path, "r") as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)


def process_input(input_str):
    """
    Processes 1st param to determine the input file type and location.

    Args:
    input_str(str): A string representing the 1st param.

    Returns:
    dict: A dictionary containing the input file type and location.
    """
    # Check if input is a video file
    if re.search(r"\.(mp4|mov|avi|flv)$", input_str):
        return {"type": "video", "path": input_str}

    # Check if input is an audio file
    elif re.search(r"\.(mp3|wav|flac|aac|m4a)$", input_str):
        return {"type": "audio", "path": input_str}

    # Check if input is a URL
    elif re.search(r"^https?:\/\/", input_str):
        return {"type": "url", "path": input_str}

    else:
        raise ValueError("Invalid input format")


def video2audio(input_file):
    """
    Converts a video file to an audio file.

    Args:
    input_file(str): The filepath of the input video file.
    """
    output_file = input_file.split(".")[0] + ".mp3"
    stream = ffmpeg.input(input_file)
    audio = stream.audio
    audio = ffmpeg.output(audio, output_file)
    ffmpeg.run(audio)


def audio2sub(audio_filename, output_ext, model, language, force=False, verbose=False):
    """
    Uses a speech recognition model to transcribe an audio file and
    generate subtitle files in various formats.

    Args:
    audio_filename(str): The filename of the audio input file.
    output_ext(str): The desired format of the output subtitle file(s).
                    Can be "txt", "srt", "vtt", "tsv", or "json".
    model(str): The name/path to the speech recognition model
                to be used for transcription.
    language(str): The language code of the audio file to be transcribed
                    (e.g. "en").
    force(bool): An optional flag indicating whether to overwrite any existing output
                files.
    verbose(bool): An optional flag indicating whether to print additional information
                during processing.
    """
    audio_filepath = os.path.join(os.getcwd(), audio_filename)
    output_filename = audio_filename.split(".")[0] + "." + output_ext
    if not os.path.exists(output_filename) or force:
        model = whisper.load_model(model)
        transcription_response = model.transcribe(
            audio_filepath, language=language, verbose=True
        )
        output_writer = whisper.utils.get_writer(output_ext, "./")
        output_writer(transcription_response, audio_filename)


def url2sub(video_url, output_ext, model, language, proxy, force=False, verbose=False):
    """
    Download subtitles for a given video URL directly or
    download audio then convert to subtitle using the given model.

    Args:
        video_url (str): URL/path of the video.
        output_ext (str): Extension of the output subtitle file.
        model (obj): Model used for converting audio to subtitle.
        language (str): Language code of the subtitle.
        proxy (str): Proxy to be used for downloading the video.
        force (bool, optional): Whether to force download the audio file
                                even if it already exists. Defaults to False.
        verbose (bool, optional): Whether to print detailed logs
                                during the download process. Defaults to False.
    """
    # Options for downloading subtitles
    ydl_opts = {
        "writesubtitles": True,
        "skip_download": True,
        "subtitleslangs": language,
        "outtmpl": "%(title).150B.%(ext)s",
        "quiet": verbose,
        "proxy": proxy,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(video_url, download=False)
            mp3_filename = ydl.prepare_filename(info_dict).split(".")[0] + ".mp3"
            mp3_filepath = os.path.join(os.getcwd(), mp3_filename)
            # Check if subtitles are available in given language
            if (
                info_dict["requested_subtitles"]
                and language in info_dict["requested_subtitles"]
            ):
                # Download subtitle
                ydl.download(video_url)
            else:
                print(f"No {language} subtitle found, downloading mp3...")
                if not os.path.exists(mp3_filepath) or force:
                    # yt-dlp options for audio download
                    ydl_opts = {
                        "format": "bestaudio/best",
                        "postprocessors": [
                            {
                                "key": "FFmpegExtractAudio",
                                "preferredcodec": "mp3",
                                "preferredquality": "192",
                            }
                        ],
                        "outtmpl": "%(title).150B.%(ext)s",
                        "quiet": verbose,
                        "proxy": proxy,
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download(video_url)
                    print(f"{mp3_filename} has been downloaded.")
                # Convert audio to subtitle using given model
                audio2sub(mp3_filename, output_ext, model, language, force, verbose)
        except Exception as e:
            print(e)
