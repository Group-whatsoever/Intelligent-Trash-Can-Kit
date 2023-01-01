import configparser
import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

LED = 17

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

GPIO.setup(LED, GPIO.OUT)

config = configparser.ConfigParser()
config.read("config.ini")
critical_distance = int(config["UltrasonicSensor"]["CriticalDistance"])


def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance


if __name__ == "__main__":
    try:
        while True:
            dist = distance()
            print("Ultrasonic Sensor: Measured Distance = %.1f cm" % dist)
            if dist > critical_distance:
                # write status to status.txt
                with open("status.txt", "w") as f:
                    f.write("0")
                print('LED: ON')
                GPIO.output(LED, GPIO.HIGH)
            else:
                with open("status.txt", "w") as f:
                    f.write("1")
                print('LED: OFF')
                GPIO.output(LED, GPIO.LOW)
            with open("distance.txt", "w") as f:
                f.write(str(dist))
            time.sleep(1)

    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Ultrasonic Sensor and LED: Cleaned Up")
