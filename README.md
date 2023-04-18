# video2sub

video2sub is a command-line tool that transcribes video/audio/url to subtitles. It supports various subtitle formats such as txt, srt, vtt, tsv, and json. The tool uses speech recognition models from [whisper](https://github.com/openai/whisper) to perform transcription.

## Requirements

Python 3.8+  
CUDA supported GPU

## Installation

Install [pipx](https://github.com/pypa/pipx)

Install video2sub using pipx:

```sh
pipx install video2sub --include-deps
```

(Optional) Copy `config.example.yml` to `~/.config/` then rename it to `config.yml`. Edit it to your prefer default value.

## Usage

```sh
video2sub [video_url] [--lang] [--model] [--proxy] [--output] [--verbose] [--force]
```

|Argument|Description|
|---|---|
|video_url|The URL of the video or path of the video/audio file.|
|--lang|The language code of the audio file to be transcribed. Default: "en".|
|--model|The name/path to the speech recognition model to be used for transcription. Default: "small".|
|--proxy|Proxy to be used for downloading the video from url.|
|--output|Output format: txt, vtt, srt, tsv, json. Default: "txt".|
|--verbose|Show output.|
|--force|Force to retrieve then transcribe video regardless of existing audio or subtitle file.|
Note: If the --lang or --model arguments are not specified, the tool will use the default values which can be set by the user in the configuration file `~/.config/video2txt.yml`.

## Examples

1. Transcribe a video from a URL using default config:

    ```sh
    video2sub https://www.youtube.com/watch?v=dQw4w9WgXcQ
    ```

1. Transcribe a video from a English spoken video file using medium model and save it as a .vtt subtitle:

    ```sh
    video2sub my_video.mp4 --lang en --model medium --output vtt
    ```

1. Transcribe an audio file and save it as a .srt subtitle:

    ```sh
    video2sub my_audio.mp3 --output srt
    ```
