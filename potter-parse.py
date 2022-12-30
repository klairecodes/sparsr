import cv2
import webvtt
from datetime import datetime

# this value is 1900 instead of 1970 because that is what webvtt defines as epoch
epoch_time = datetime(1900, 1, 1)

def getCapWithPhrase(phrase):
    subs_with_phrase = []
    for caption in webvtt.read("IMG_0733.MOV.vtt"):
        if caption.text.find(phrase) >= 0:
            subs_with_phrase.append(caption.text)
            print(caption.start)
    return subs_with_phrase

def main():
    # timestamps that contain the words we are looking for
    timestamps = getCapWithPhrase("this")
    
    # for ts in timestamps:
        # video = cv2.VideoCapture("/data/IMG_0733.MOV")
    # ts format: 00:00.000
    ts = "00:43:02.560"
    time = datetime.strptime(ts, "%H:%M:%S.%f")
    seconds = (time-epoch_time).total_seconds()

    video = cv2.VideoCapture("/data/IMG_0733.MOV")
    # * 1000 because milliseconds
    print(seconds*1000)
    # video.set(cv2.CAP_PROP_POS_MSEC,seconds*1000)
    video.set(cv2.CAP_PROP_POS_MSEC,1000)
    success, image = video.read()
    if success:
        print("success")
        cv2.putText(
                image,
                "here's some test text",
                (255,500),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (209, 80, 0, 255),
                3
                )
        cv2.imwrite("/data/frame.jpg", image)

    print(open("/data/IMG_0733.MOV"))

main()
