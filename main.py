import cv2
import time
import gpio
import datetime
from utils import get_contours
import glob_vars as gv

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier("frontalface_default.xml")
body_cascade = cv2.CascadeClassifier("fullbody.xml")

frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")


def run():
    detection = False
    detection_stopped_time = None
    timer_started = False
    out = None
    _, frame_old = cap.read()
    while True:
        _, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = [] if not gv.DETECT_FACES else face_cascade.detectMultiScale(gray, 1.1, 5)
        bodies = [] if not gv.DETECT_BODIES else face_cascade.detectMultiScale(gray, 1.3, 5)
        contours = [] if not gv.DETECT_CONTOURS else get_contours(frame, frame_old, gv.CONTOUR_MIN_AREA)

        if len(faces) + len(bodies) + len(contours) > 0:
            if detection:
                timer_started = False
            else:
                detection = True
                current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
                out = cv2.VideoWriter(f'{current_time}.mp4', fourcc, 20, frame_size)
        elif detection and out:
            if timer_started:
                duration = time.time() - detection_stopped_time
                if duration >= gv.SECONDS_RECORDING_AFTER_DETECTION:
                    detection = False
                    timer_started = False
                    out.release()
                    out = None
            else:
                timer_started = True
                detection_stopped_time = time.time()
        if detection:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame_rgb)

        cv2.imshow('Camera view', frame)
        if cv2.waitKey(10) == ord('q'):
            break
        frame_old = frame

    cap.release()


def main():
    try:
        gpio.init()
        gpio.set_red_led(True)
        run()
        gpio.cleanup()
    except KeyboardInterrupt:
        gpio.cleanup()


if __name__ == "__main__":
    main()
