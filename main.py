import cv2
import time
import datetime
from utils import getcontours
import glob_vars

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_fullbody.xml")

detection = False
detection_stopped_time = None
timer_started = False

frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

_, frame_old = cap.read()
while True:
    _, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = [] if not glob_vars.DETECT_FACES else face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = [] if not glob_vars.DETECT_BODIES else face_cascade.detectMultiScale(gray, 1.3, 5)
    contours = [] if not glob_vars.DETECT_CONTOURS else getcontours(frame, frame_old, glob_vars.CONTOUR_MIN_AREA)

    if len(faces) + len(bodies) + len(contours) > 0:
        if detection:
            timer_started = False
        else:
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter(f"{current_time}.mp4", fourcc, 20, frame_size)
    elif detection:
        if timer_started:
            duration = time.time() - detection_stopped_time
            if  duration >= glob_vars.SECONDS_RECORDING_AFTER_DETECTION:
                detection = False
                timer_started = False
                out.release()
        else:
            timer_started = True
            detection_stopped_time = time.time()

    if detection:
        out.write(frame)
        
    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) == ord('q'):
        break
    frame_old = frame

if not out: out.release()
cap.release()
cv2.destroyAllWindows()