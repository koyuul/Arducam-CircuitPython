import board
import busio
from digitalio import DigitalInOut, Direction
from time import sleep
from camera import *
# These work for Google Coral. Please refer to your board's pinout and your wiring to match.
# You can also try print(dir(board)) to view what you have.
CLOCK_PIN = board.ECSPI1_SCLK
MISO_PIN = board.ECSPI1_MISO
MOSI_PIN = board.ECSPI1_MOSI
GPIO_PIN = board.GPIO_P37

BAUDRATE = 8000000

# refer to camera.py for possible resolutions
USER_RES = '1920x1080'


'''
idea: we need a class that will:
- take in a list of camera controller commands
- parse each command
- execute them in that order
'''

class CameraController:
    def __init__(self, commands):
        # break down commands here. for now we static set it
        command = ["STD_CAPTURE|1000|1731042297"]
        self.commands = command
        self.camera_init() # init self.camera

    def camera_init(self):
        spi = busio.SPI(clock=CLOCK_PIN, MISO=MISO_PIN, MOSI=MOSI_PIN)
        # Lock SPI bus before configuring baudrate
        if spi.try_lock():
            try:
                spi.configure(baudrate=BAUDRATE)
            finally:
                spi.unlock()
        else:
            print("Could not lock SPI bus") #TODO: handle this error better...
            exit()

        cs = DigitalInOut(GPIO_PIN)
        cs.direction = digitalio.Direction.OUTPUT  # Set CS pin as output
        self.camera = Camera(spi, cs)
        self.camera.resolution = USER_RES
    
    def execute(self):
        for command in self.commands:
            attributes = command.split("|")
            operation = attributes[0]
            if (operation == "STD_CAPTURE"):
                    camera_enable_code = attributes[1]
                    epoch = attributes[2]
                    print("capture")

cc = CameraController(["temp"])
cc.execute()
# cam.capture_jpg()
# sleep(0.05)
# cam.saveJPG('image.jpg')