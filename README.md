# NOTE
This is a branch from Core Electronic's MicroPython Repo, porting it over to CircuitPython. 

This was built for and tested on Google Coral, however I'd guess it'd work on other linux SBC's (if using a Pi use ArduCam's drivers). If you do get it to work on a different board let me know! 

It is likely possible/better to port over ArduCam's SDK somehow, but I never got a response from their suppport email so this seemed like the best alternative. If anyone has any advice on that... also let me know!

### How to use
Just execute the `main.py` file. Be sure to change the pins to however you set your board up. The default setup uses `SPI0` and pin 37 for the GPIO pin. Currently this only snaps a single image, but should be implemented easily enough.

### Also Experimental
Similar to the repo this branches from, it's still extremely experimental at this point. Just wanted to upload this incase anyone is/was in my position.

Current drawback/room for improvement:
- Capturing anything higher than 480p is EXTREMELY slow. should be fixable
- Still lacks a couple of features that Arducam's drivers do, Core Electronic's port doesn't yet have them implemented either.
- Honestly code is kind of a mess (my fault). a good starting point though!
- camera.py code for burst images haven't been looked at. Will need to be changed if you want to use it.

### future task list
- [ ] decrease save time (by batching)
- [ ] implement some sorta filename save structure eg img1, img2 ...
- [ ] increase picture snapping time (exposure)
- [ ] clean up print statements, make optional?
- [ ] work this into our cpp project strcuture (personal proj)
- [ ] figure out how this is gonna work with multiple cams...
- [ ] keep in check with CoreElectronic's version (tackle some of their TODOs?)

# ORIGINAL REPO's README (REFER TO THEIR REPO FOR MOST UPDATED README):
This is the Repo for the Core Electronics port of the Arducam Mega Cameras for the Raspberry Pi Pico (Micropython)
* [ArduCam Mega 5MP Camera](https://core-electronics.com.au/arducam-mega-5mp-camera.html)
* [ArduCam Mega 3MP Camera](https://core-electronics.com.au/arducam-mega-3mp-camera.html)

Status: **Experimental**
This driver is very much experimental at the moment. Expect frequent, breaking updates.
This project is featured in the 27-July-2023 episode of [The Factory](https://youtu.be/M_b3kmnjF9Y) - Core Electronics' Engineering and Product Development vlog.

<a href="http://www.youtube.com/watch?feature=player_embedded&v=M_b3kmnjF9Y" target="_blank">
 <img src="http://img.youtube.com/vi/M_b3kmnjF9Y/mqdefault.jpg" alt="Watch the video" width="240" height="180" border="10" />
</a>

Project Status:
- [x] Confirmed working on 3MP Camera and 5MP Camera
- [x] SOLVED: Photos have a green hue, camera_idx identifies the two versions - https://forum.arducam.com/t/mega-3mp-micropython-driver/5708
- [x] Can set resolution
- [ ] Can set remaining filters and modes
- [ ] Able to set multiple adjustments at the same time ([see issue#3](https://github.com/CoreElectronics/CE-Arducam-MicroPython/issues))
- [ ] Class moved to separate file
- [ ] Burst read - decrease time to save photo
- [ ] Set SPI Speed higher - decrease time to save photo - Recommended speed from ArduCam 800000 baud, need to implement a check on init
- [ ] Confirm a micro SD card can use the same SPI bus (Micropython compatibility) - requires camera to release SPI bus, bulk reading/writing into bytearray would speed this up
- [ ] Confirm working with the latest Micropython version
- [ ] Filemanager also handles subfolders for images - Requires examples
- [ ] Confirm that different file formats output correctly (RGB=BMP, YGV?)
- [ ] Confirm that pixel RGB values can be extrapolated from BMP format for machine learning applications

The Camera library can be created by extracting the 'Camera' class from the [main.py](https://github.com/CoreElectronics/CE-Arducam-MicroPython/blob/main/main.py) file.

# License
This project is open source - please review the LICENSE.md file for further licensing information.

If you have any technical questions, or concerns about licensing, please contact technical support on the [Core Electronics forums](https://forum.core-electronics.com.au/).
