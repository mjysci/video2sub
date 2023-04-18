import argparse
from .utils import get_config, process_input, url2sub, video2audio, audio2sub

# Get default configuration values
default_args = get_config()

# Create argument parser for CLI
parser = argparse.ArgumentParser(description="video_url --lang --model --force")
parser.add_argument(
    "video_url", type=str, help="Video URL or path of the video/audio file."
)
parser.add_argument(
    "--lang",
    type=str,
    default=default_args.get("lang", "en"),
    nargs="?",
    help="The language code of the audio file to be transcribed. Default: en.",
)
parser.add_argument(
    "--model",
    type=str,
    default=default_args.get("model", "small"),
    nargs="?",
    help="The name/path to the speech recognition model to be used for transcription. \
        Default: small",
)
parser.add_argument(
    "--proxy",
    type=str,
    default=default_args.get("proxy", ""),
    nargs="?",
    help="Proxy to be used for downloading the video from url.",
)
parser.add_argument(
    "--output",
    type=str,
    default=default_args.get("output", "txt"),
    nargs="?",
    help="Output format: txt, vtt, srt, tsv, json. Default: txt",
)
parser.add_argument("--verbose", action="store_true", help="Show output")
parser.add_argument(
    "--force",
    action="store_true",
    help="Force to retrieve then transcribe video \
        regardless of existing audio or subtitle file.",
)
args = parser.parse_args()


def video2sub():
    """
    Transcribe url, video or audio file to subtitles.
    """
    path_dict = process_input(args.video_url)
    if path_dict["type"] == "url":
        url2sub(
            path_dict["path"],
            args.output,
            args.model,
            args.lang,
            args.proxy,
            args.force,
            args.verbose,
        )

    elif path_dict["type"] == "video":
        video2audio(path_dict["path"])
        mp3_filename = path_dict["path"].split(".")[0] + ".mp3"
        audio2sub(
            mp3_filename, args.output, args.model, args.lang, args.force, args.verbose
        )

    elif path_dict["type"] == "audio":
        audio2sub(
            path_dict["path"],
            args.output,
            args.model,
            args.lang,
            args.force,
            args.verbose,
        )


if __name__ == "__main__":
    video2sub()
