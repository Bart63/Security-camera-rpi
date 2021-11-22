import cv2
import sys
import time
import gpio
import datetime
from utils import get_contours
import user_view as uv
import notification as notify

cv2.useOptimized()

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
        USER_SETTINGS = uv.get_vars()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = [] if not USER_SETTINGS['DETECT_FACES'] else face_cascade.detectMultiScale(gray, 1.1, 5)
        bodies = [] if not USER_SETTINGS['DETECT_BODIES'] else face_cascade.detectMultiScale(gray, 1.3, 5)
        contours = [] if not USER_SETTINGS['DETECT_CONTOURS'] else get_contours(frame, frame_old, USER_SETTINGS['CONTOUR_MIN_AREA'])

        print(len(faces), len(bodies), len(contours))
        if len(faces) + len(bodies) + len(contours) > 0:
            if detection:
                timer_started = False
            else:
                gpio.set_red_led(True)
                detection = True
                gpio.set_buzzer(True)
                detection_stopped_time = time.time()
                current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
                notify.email_alert(f"Wlamanie {current_time}", f"{current_time} rozpoczeto rejestrowac zdarzenie", "mail@temp")
                notify.send_sms_via_email(f"{current_time} rozpoczeto rejestrowac zdarzenie", "mail@temp")
                out = cv2.VideoWriter(f'{current_time}.mp4', fourcc, 20, frame_size)
        elif detection and out:
            if timer_started:
                duration = time.time() - detection_stopped_time
                if duration >= USER_SETTINGS['SECONDS_RECORDING_AFTER_DETECTION']:
                    detection = False
                    gpio.set_buzzer(False)
                    timer_started = False
                    out.release()
                    out = None
                    gpio.set_red_led(False)
            else:
                timer_started = True
        if detection:
            out.write(frame)

        if len(sys.argv) == 2 and sys.argv[1] == 'debug':
            cv2.imshow('Camera view', frame)
            if cv2.waitKey(10) == ord('q'):
                cv2.destroyAllWindows()
                break
        frame_old = frame
    cap.release()


def main():
    try:
        gpio.init()
        gpio.set_green_led(True)
        run()
        gpio.cleanup()
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        cap.release()
        gpio.cleanup()


if __name__ == "__main__":
    main()
