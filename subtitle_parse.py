""" This program parses vtt caption files and returns frames containing the provided expression."""
import sys
from datetime import datetime
import argparse
import cv2
import webvtt

# this value is 1900 instead of 1970 because that is what webvtt defines as epoch
EPOCH_TIME = datetime(1900, 1, 1)

def get_cap_with_phrase(captions_file, phrase):
    """Parses the vtt caption file to get each caption containing "phrase"."""
    subs_with_phrase = []
    for caption in webvtt.read(captions_file):
        if caption.text.find(phrase) >= 0:
            subs_with_phrase.append(caption)
    return subs_with_phrase

def get_frames(captions, video):
    """Looks through the video timestamps, and outputs the frame with its caption to a file."""
    for caption in captions:
        timestamp = caption.start # format: 00:00:00.000
        time = datetime.strptime(timestamp, "%H:%M:%S.%f")
        seconds = (time-EPOCH_TIME).total_seconds() # subtraction converts to correct type

        video.set(cv2.CAP_PROP_POS_MSEC, seconds*1000) # milliseconds
        success, image = video.read()
        if success:
            output_frames(caption, image, int(seconds))

def get_frames_range(captions, video, padding):
    """Looks through the video at each timestamp, and outputs the frame and a "padding" range of fr\
            ames with their captions to several files."""
    for caption in captions:
        timestamp = caption.start # format: 00:00:00.000
        time = datetime.strptime(timestamp, "%H:%M:%S.%f")
        seconds = (time-EPOCH_TIME).total_seconds() # subtraction converts to correct type
        for secs in range(int(seconds)-padding, int(seconds)+padding+1):
            video.set(cv2.CAP_PROP_POS_MSEC, secs*1000)
            success, image = video.read()
            if success:
                output_frames(caption, image, secs)

def output_frames(caption, image, seconds):
    """Outputs the provided caption and image to an image file."""
    # TODO: remove hardcoded positioning
    # Weird string slicing is to handle out-of-order seconds
    print(f"Outputting frame-{caption.start[:6]}{seconds}{caption.start[8:]}.jpg...")
    # black text drawn behind for outline
    cv2.putText(
        image,                      # image object
        caption.text,               # text to put
        (255, 1000),                 # origin/position
        cv2.FONT_HERSHEY_SIMPLEX,   # font
        1,                          # font scale
        (0, 0, 0),                  # font color (BGR format)
        cv2.LINE_AA,                # line type
        3                           # thickness
        )
    # white text
    cv2.putText(
        image,
        caption.text,
        (255, 1000),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
        )
    cv2.imwrite(f"/data/frames/frame-{caption.start}-{seconds}.jpg", image)

def main():
    """Driver of the program."""
    try:
        # Parsing CLI arguments
        parser = argparse.ArgumentParser(
            prog="caption-parser",
            description="A program to return screenshots of vtt captioned videos containing a certa\
                    in phrase."
            )
        parser.add_argument("-f", "--filename", type=str, required=True,
                            help="Video file to search through.")
        # TODO: figure out how to make default subtitles_file the filename with a .vtt extension without parsing with argparse twice (and using namespaces)
        parser.add_argument("-s", "--subtitles_file", type=str,
                            help="Separate subtitle file to use. Default is the provided video file\
                                    name with a .vtt extension.")
        parser.add_argument("-e", "--expression", type=str, required=True,
                            help="Expression to search for.")
        parser.add_argument("-p", "--padding", type=int, default=0,
                            help="Adds n frames per second before and after the matched frames.")

        args = parser.parse_args()
        filename = args.filename
        subtitles_file = args.subtitles_file
        if subtitles_file is None:
            # subtitles_file = f"{os.path.splitext(filename)[0]}.vtt"
            subtitles_file = f"{filename}.vtt"
        expression = args.expression
        padding = args.padding

        # timestamps that contain the words we are looking for
        captions = get_cap_with_phrase(subtitles_file, expression)
        video = cv2.VideoCapture(filename)
        if padding > 0:
            get_frames_range(captions, video, padding)
        elif padding < 0:
            raise Exception("Error: padding value cannot be negative.")
        else:
            get_frames(captions, video)

    except KeyboardInterrupt:
        print("Operation cancelled by keyboard interrupt.")
    except Exception as exception:
        print(exception)
    finally:
        sys.exit()

main()
