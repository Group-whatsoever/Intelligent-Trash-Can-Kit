import configparser
import RPi.GPIO as GPIO
from time import sleep

# Enable pin from controller
EN = 33
# Direction pin from controller
DIR = 31
# Step pin from controller
STEP = 29
# 0/1 used to signify clockwise or counterclockwise.
CW = 1
CCW = 0

IR = 16

# Setup pin layout on PI
GPIO.setmode(GPIO.BOARD)

# Establish Pins in software
GPIO.setup(EN, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

# Set the enable pin to low to enable the stepper
GPIO.output(EN, 0)

# Set the first direction you want it to spin
GPIO.output(DIR, CW)

GPIO.setup(IR, GPIO.IN)

config = configparser.ConfigParser()
config.read("config.ini")
if config["StepperMotor"]["OpenDirection"] == "CW":
    open_direction = CW
    close_direction = CCW
else:
    open_direction = CCW
    close_direction = CW
steps = int(config["StepperMotor"]["Steps"])
delay = float(config["StepperMotor"]["Delay"])


def stepper(direction, steps, delay):
    # Set the direction you want it to spin
    GPIO.output(DIR, direction)
    # Run the stepper motor
    for x in range(steps):
        # Set one coil winding to high
        GPIO.output(STEP, GPIO.HIGH)
        # Allow it to get there.
        sleep(delay)  # Dictates how fast stepper motor will run
        # Set coil winding to low
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)  # Dictates how fast stepper motor will run


try:
    # Run forever.
    while True:
        status = 0
        with open("status.txt", "r") as f:
            status = f.read()
            print(status)
            if status == "":
                continue
            else:
                status = int(status)
        if GPIO.input(IR) == 0 and status == 0:
            print("Infrared Sensor: People Detected")
            print("Stepper Motor: Opening")
            stepper(open_direction, steps, delay)
            sleep(1)
            while GPIO.input(IR) == 0:
                sleep(1)
            print("Infrared Sensor: No People Detected")
            print("Stepper Motor: Closing")
            stepper(close_direction, steps, delay)

# Once finished clean everything up
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Stepper Motor and Infrared Sensor: Cleaned Up")
