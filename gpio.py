import RPi.GPIO as GPIO
import glob_vars as gv


def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gv.GREEN_LED, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(gv.RED_LED, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(gv.BUZZER, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(gv.BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def set_green_led(is_on: bool):
    GPIO.output(gv.GREEN_LED, GPIO.HIGH if is_on else GPIO.LOW)


def set_red_led(is_on: bool):
    GPIO.output(gv.RED_LED, GPIO.HIGH if is_on else GPIO.LOW)


def set_buzzer(is_on: bool):
    GPIO.output(gv.RED_LED, GPIO.LOW if is_on else GPIO.HIGH)


def cleanup():
    GPIO.cleanup()
