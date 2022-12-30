import cv2
import webvtt
from datetime import datetime

# this value is 1900 instead of 1970 because that is what webvtt defines as epoch
epoch_time = datetime(1900, 1, 1)

def getCapWithPhrase(phrase):
    subs_with_phrase = []
    # TODO: replace with data/IMG_0733.MOV.vtt
    for caption in webvtt.read("/data/IMG_0733.MOV.vtt"):
        if caption.text.find(phrase) >= 0:
            subs_with_phrase.append(caption)
    return subs_with_phrase

def main():
    # timestamps that contain the words we are looking for
    captions = getCapWithPhrase("this")
    video = cv2.VideoCapture("/data/IMG_0733.MOV")
    
    for caption in captions:
        ts = caption.start # format: 00:00:00.000
        text = caption.text
        time = datetime.strptime(ts, "%H:%M:%S.%f")
        seconds = (time-epoch_time).total_seconds() # subtraction converts to correct type

        video.set(cv2.CAP_PROP_POS_MSEC,seconds*1000) # milliseconds
        success, image = video.read()
        if success:
            print(f"Outputting frame-{caption.start}.jpg...")
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
            cv2.imwrite(f"/data/frames/frame-{caption.start}.jpg", image)
main()
