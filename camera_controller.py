import board
import busio
import os
import sqlite3
from digitalio import DigitalInOut, Direction
from time import sleep
from datetime import datetime
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
    def __init__(self, commands):
        self.commands = commands

        # Connect to (or create if needed) the metadata database
        self.conn = sqlite3.connect("./image_info.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS metadata (
                image_id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_path TEXT NOT NULL,
                request_time TEXT, -- SQLite doesnt have datetimes, but this is always stored as ISO8601 to query efficiently
                capture_time TEXT, -- SQLite doesnt have datetimes, but this is always stored as ISO8601 to query efficiently
                camera_source INTEGER,
                location_prediction TEXT, -- This should change based on what location prediction features we do
                has_earth INTEGER, -- SQLite doesnt have integers, so store this as 1=True 0=False
                has_space INTEGER -- SQLite doesnt have integers, so store this as 1=True 0=False,
            )
        ''')
        self.conn.commit()

        self.camera_init() # init self.camera

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
            print("Could not lock SPI bus") #TODO: handle this error better...
            exit()
        
        # Initialize a camera object
        cs = DigitalInOut(GPIO_PIN)
        cs.direction = digitalio.Direction.OUTPUT  # Set CS pin as output
        self.camera = Camera(spi, cs)
        self.camera.resolution = USER_RES
    
    def execute(self):
        for command in self.commands:
            attributes = command.split("|")
            operation = attributes[0]
            if (operation == "STD_CAPTURE"): # take a single image capture
                    print("STD_CAPTURE")
                    camera_enable_code = attributes[1]
                    request_epoch = attributes[2]

                    # TODO: add functionality for multiple captures
                    
                    # Capture the image (into the arducam's buffer), and note the time it was taken
                    # self.camera.capture_jpg()
                    capture_epoch = int(datetime.now(tz=datetime.timezone.utc).timestamp())
                    sleep(0.05)

                    image_metadata = {
                        # image_id is automatically incrementally set
                        "image_path": "", # Temporarily unset until we find the image_id
                        "request_epoch": request_epoch,
                        "capture_epoch": capture_epochs,
                        "camera_soruce": 1, # TODO: this should change based on requested cameras
                    }

                    # Enter image metadata into the metadata table.
                    self.cursor.execute(
                        "INSERT INTO metadata(image_path, request_epoch, capture_epoch, camera_source) VALUES(?, ?, ?, ?)",
                        ( image_metadata["image_path"], image_metadata["request_epoch"], image_metadata["capture_epoch"], image_metadata["camera_source"] )
                    )

                    # Get the image_id, create the path, and save it
                    image_id = self.cursor.lastrowid
                    image_folder = f"{os.path.expanduser("~/images")}/{image_id}"
                    image_path = f"{image_folder}/{image_id}.jpg"
                    os.makedirs(image_folder, exist_ok=True)
                    self.camera.saveJPG(image_path)

                    # Finally, update the metadata row to contain the path and commit all changes
                    self.cursor.execute("UPDATE metadata SET image_path = ? where image_id = ?", (image_path, image_id))
                    self.conn.commit()

                    print(f"Completed the request received at {request_epoch}, captured at {capture_epoch}. Saved into {image_path}.")
            if (operation == "RETRIEVE)"):
                !TODO! WE WRITE THIS NEXT!! :)
    
    def retrieve(self, image_id=None, request_epoch=None, capture_epoch=None, look_before_epoch=False, predicted_location=None):
        if (image_id is not None):
            self.cursor.execute(f"SELECT * FROM metadata WHERE image_id=?", (image_id))
        else if (request_epoch is not None):
            # Find closest desired timestamp. Need to find this first to get all images taken at that time (mult. cameras take images at once)
            closest_result = None
            if (look_before_epoch == True): # Find closest timestamp to given timestamp, before or after
                self.cursor.execute("SELECT request_epoch FROM metadata ORDER BY ABS(request_epoch - ?) ASC LIMIT 1", (request_epoch))
                closest_result = self.cursor.fetchone()
            else: # Find closest timestamp at or after given timestamp
                self.cursor.execute("SELECT request_epoch FROM metadata WHERE request_epoch >= ? ORDER BY request_epoch ASC LIMIT 1", (request_epoch))
                closest_result = self.cursor.fetchone()
            self.cursor.execute("SELECT * FROM metadata WHERE request_epoch = ?", (closest_result))
        else if (capture_epoch is not None):
                        closest_result = None
            if (look_before_epoch == True): # Find closest timestamp to given timestamp, before or after
                self.cursor.execute("SELECT capture_epoch FROM metadata ORDER BY ABS(capture_epoch - ?) ASC LIMIT 1", (capture_epoch))
                closest_result = self.cursor.fetchone()
            else: # Find closest timestamp at or after given timestamp
                self.cursor.execute("SELECT capture_epoch FROM metadata WHERE capture_epoch >= ? ORDER BY capture_epoch ASC LIMIT 1", (capture_epoch))
                closest_result = self.cursor.fetchone()
            self.cursor.execute("SELECT * FROM metadata WHERE capture_epoch = ?", (closest_result))
        else if (predicted_location is not None):
            print("TODO: Handle this later...") # TODO: handle a predicted location
        else:
            print("TODO: Handle no filters...") # TODO: Handle no filters provided

        results = self.cursor.fetchall()
        return results # TODO: figure out how to return this 
            




cc = CameraController(["STD_CAPTURE|1000|1731042297"]) # Currently a hardcoded example command
cc.execute()