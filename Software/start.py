from time import sleep
from subprocess import Popen

process_list = []

try:
    # Start ultrasonic sensor and LED
    ultrasonic_sensor_and_led = Popen(["python3", "ultrasonic_sensor_and_led.py"])
    process_list.append(ultrasonic_sensor_and_led)

    sleep(0.5)

    # Start stepper motor and infrared sensor
    stepper_motor_and_infrared_sensor = Popen(
        ["python3", "stepper_motor_and_infrared_sensor.py"]
    )
    process_list.append(stepper_motor_and_infrared_sensor)

    # Wait for keyboard interrupt
    while True:
        pass
except KeyboardInterrupt:
    print("Keyboard Interrupt")
    for process in process_list:
        process.terminate()
