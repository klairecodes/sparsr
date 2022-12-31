import cv2
import webvtt
from datetime import datetime

# this value is 1900 instead of 1970 because that is what webvtt defines as epoch
epoch_time = datetime(1900, 1, 1)

"""
Parses the vtt caption file to get each caption containing "phrase".
"""
def getCapWithPhrase(phrase):
    subs_with_phrase = []
    for caption in webvtt.read("/data/IMG_0733.MOV.vtt"):
        if caption.text.find(phrase) >= 0:
            subs_with_phrase.append(caption)
    return subs_with_phrase

"""
Looks through the video at each timestamp, and outputs the frame with its caption to a file.
"""
def getFrames(captions, video):
    for caption in captions:
        ts = caption.start # format: 00:00:00.000
        text = caption.text
        time = datetime.strptime(ts, "%H:%M:%S.%f")
        seconds = (time-epoch_time).total_seconds() # subtraction converts to correct type

        video.set(cv2.CAP_PROP_POS_MSEC,seconds*1000) # milliseconds
        success, image = video.read()
        if success:
            outputFrames(caption, image, int(seconds))

"""
Looks through the video at each timestamp, and outputs the frame and a "padding" range of frames with their captions to several files.
"""
def getFramesRange(captions, video, padding):
    for caption in captions:
        ts = caption.start # format: 00:00:00.000
        text = caption.text
        time = datetime.strptime(ts, "%H:%M:%S.%f")
        seconds = (time-epoch_time).total_seconds() # subtraction converts to correct type
        for secs in range(int(seconds)-padding, int(seconds)+padding+1):
            print(f"sec:{secs}")
            video.set(cv2.CAP_PROP_POS_MSEC,secs*1000)
            success, image = video.read()
            if success:
                outputFrames(caption, image, secs)

"""
Outputs the provided caption and image to an image file.
"""
def outputFrames(caption, image, seconds):
        # TODO: remove hardcoded positioning
        # Weird string slicing is to handle out-of-order seconds
        print(f"Outputting frame-{caption.start[:6]}{seconds}{caption.start[8:]}.jpg...")
        # black text drawn behind for outline
        cv2.putText(
                image,                      # image object
                caption.text,               # text to put
                (255,1000),                 # origin/position
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
                (255,1000),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
                )
        cv2.imwrite(f"/data/frames/frame-{caption.start}-{seconds}.jpg", image)

def main():
    # timestamps that contain the words we are looking for
    captions = getCapWithPhrase("this")
    video = cv2.VideoCapture("/data/IMG_0733.MOV")
    getFrames(captions, video)
    
main()
