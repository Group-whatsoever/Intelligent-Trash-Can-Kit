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
        command = input("> ").split(" ")
        if len(command) == 3:
            if command[0] == "CW":
                direction = CW
            elif command[0] == "CCW":
                direction = CCW
            else:
                print("Invalid Command")
                continue
            steps = int(command[1])
            delay = float(command[2])
            stepper(direction, steps, delay)
        elif len(command) == 1:
            if command[0] == "ENABLE":
                GPIO.output(EN, 0)
            elif command[0] == "DISABLE":
                GPIO.output(EN, 1)
            elif command[0] == "HELP":
                print("Commands:")
                print("    CW <steps> <delay>")
                print("    CCW <steps> <delay>")
                print("    ENABLE")
                print("    DISABLE")
            else:
                print("Invalid Command")
        else:
            print("Invalid Command")

# Once finished clean everything up
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Stepper Motor: Cleaned Up")
