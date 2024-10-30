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

spi = busio.SPI(clock=CLOCK_PIN, MISO=MISO_PIN, MOSI=MOSI_PIN)

# Lock SPI bus before configuring baudrate
if spi.try_lock():
    try:
        spi.configure(baudrate=BAUDRATE)
    finally:
        spi.unlock()
else:
    print("Could not lock SPI bus")
    exit()

cs = DigitalInOut(GPIO_PIN)
cs.direction = digitalio.Direction.OUTPUT  # Set CS pin as output

cam = Camera(spi, cs)

cam.resolution = USER_RES

cam.capture_jpg()
sleep(0.05)
cam.saveJPG('image.jpg')