import board
import busio
import os
import sqlite3
import sys
from digitalio import DigitalInOut, Direction
from time import sleep
from datetime import datetime, timezone
from camera import *

# These pins work for Google Coral. Please refer to your board's pinout and your wiring to match.
# You can also try print(dir(board)) to view what you have.
CLOCK_PIN = board.ECSPI1_SCLK
MISO_PIN = board.ECSPI1_MISO
MOSI_PIN = board.ECSPI1_MOSI
GPIO_PIN = board.GPIO_P37

BAUDRATE = 8000000

# refer to camera.py for possible resolutions
USER_RES = '1920x1080'

class CameraController:
    def __init__(self):
        # Connect to (or create if needed) the metadata database
        self.conn = sqlite3.connect("/home/mendel/tes-camera/image_info.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS metadata (
                image_id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_path TEXT NOT NULL,
                request_epoch INTEGER,
                capture_epoch INTEGER,
                camera_source INTEGER,
                location_prediction TEXT, -- This should change based on what location prediction features we do
                has_earth INTEGER, -- SQLite doesnt have integers, so store this as 1=True 0=False
                has_space INTEGER -- SQLite doesnt have integers, so store this as 1=True 0=False,
            )
        ''')
        self.conn.commit()
        self.camera_init()

    def camera_init(self):
        # Initiate a connection to the SPI Bus we're using
        spi = busio.SPI(clock=CLOCK_PIN, MISO=MISO_PIN, MOSI=MOSI_PIN)

        # Lock SPI bus before configuring baudrate
        if spi.try_lock():
            try:
                spi.configure(baudrate=BAUDRATE)
            finally:
                spi.unlock()
        else:
            print("[CAMERA]: Could not lock SPI bus") #TODO: handle this error better...
            exit()
        
        # Initialize a camera object
        cs = DigitalInOut(GPIO_PIN)
        cs.direction = digitalio.Direction.OUTPUT  # Set CS pin as output
        self.camera = Camera(spi, cs)
        self.camera.resolution = USER_RES
    
    def execute(self):
        operation = sys.argv[1]
        if (operation == "STD_CAPTURE"): # take a single image capture
                print("[CAMERA]: Executing STD_CAPTURE...")
                camera_enable_code = sys.argv[2]
                request_epoch = sys.argv[3]

                # TODO: add functionality for multiple captures
                
                # Capture the image (into the arducam's buffer), and note the time it was taken
                self.camera.capture_jpg()
                capture_epoch = int(datetime.now(tz=timezone.utc).timestamp())
                sleep(0.05)
                print("[CAMERA]: Capture complete, now saving image. This may take a while...")

                image_metadata = {
                    # image_id is automatically incrementally set
                    "image_path": "", # Temporarily unset until we find the image_id
                    "request_epoch": request_epoch,
                    "capture_epoch": capture_epoch,
                    "camera_source": 1, # TODO: this should change based on requested cameras
                }

                # Enter image metadata into the metadata table.
                self.cursor.execute(
                    "INSERT INTO metadata(image_path, request_epoch, capture_epoch, camera_source) VALUES(?, ?, ?, ?)",
                    ( image_metadata["image_path"], image_metadata["request_epoch"], image_metadata["capture_epoch"], image_metadata["camera_source"] )
                )

                # Get the image_id, create the path, and save it
                image_id = self.cursor.lastrowid
                image_folder = f"{os.path.expanduser('~/images')}/{image_id}"
                image_path = f"{image_folder}/{image_id}.jpg"
                os.makedirs(image_folder, exist_ok=True)
                self.camera.saveJPG(image_path)

                # Finally, update the metadata row to contain the path and commit all changes
                self.cursor.execute("UPDATE metadata SET image_path = ? where image_id = ?", (image_path, image_id))
                self.conn.commit()

                print(f"[CAMERA]: Completed the request received at {request_epoch}, captured at {capture_epoch}. Saved into {image_path}.")
     # TODO: figure out how to return this 

cc = CameraController() # Currently a hardcoded example command
cc.execute()
# cc = CameraController(["STD_CAPTURE|1000|1731042297"]) # Currently a hardcoded example command