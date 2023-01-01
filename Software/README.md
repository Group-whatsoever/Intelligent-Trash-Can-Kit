# Software

## Connect wires

| Raspberry Pi 4 Model B (Board Numbering) | External Devices' Pins               |
| ---------------------------------------- | ------------------------------------ |
| 12                                       | Ultrasonic Sensor's Trigger Pin      |
| 18                                       | Ultrasonic Sensor's Echo Pin         |
| 11                                       | LED Pin                              |
| 33                                       | Stepper Motor Driver's Enable Pin    |
| 31                                       | Stepper Motor Driver's Direction Pin |
| 29                                       | Stepper Motor Driver's Pulse Pin     |
| 16                                       | Infrared Sensor's Output Pin         |

## Install dependencies

> The following commands were only tested on Raspberry Pi OS (Release date: September 22nd 2022, System: 64-bit, Kernel version: 5.15, Debian version: 11)

```shell
sudo apt update
sudo apt upgrade
sudo apt install python3-pip
sudo pip3 install RPi.GPIO
```

## Adjust `config.ini`

```shell
cd THIS_SOFTWARE_DIRECTORY
# Tune stepper motor's parameters (OpenDirection, Steps, Delay)
python3 utils/stepper_motor.py
# Tune ultrasonic sensor's parameters (CriticalDistance)
python3 utils/ultrasonic_sensor.py
# Use your favorite tool to adjust those parameters in config.ini
vim config.ini
```

## Run the software

```shell
cd THIS_SOFTWARE_DIRECTORY
python3 start.py
```