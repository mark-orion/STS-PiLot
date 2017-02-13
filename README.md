# STS-PiLot
AJAX remote control web interface with live video for the [Pimoroni STS-Pi](https://shop.pimoroni.com/products/sts-pi) and other robotics projects.
This is an educational application with the focus on keeping the code simple and understandable.
The live streaming part is based on the example code provided by Miguel Grinberg https://github.com/miguelgrinberg/flask-video-streaming. For better stability and performance network connectivity is provided by the [Gevent](http://www.gevent.org) WSGI server.

## Features
* Responsive AJAX interface for use on desktops, laptops, tablets and phones.
* Designed for [Pimoroni STS-Pi](https://shop.pimoroni.com/products/sts-pi) and [Explorer Hat Pro](https://shop.pimoroni.com/products/explorer-hat) as hardware interface, but can be adapted for other boards.
* Frontend ony requires HTML, Javascript and CSS - no proprietary plugins needed.
* Works without modification when no Raspberry Pi camera is detected - But you are missing something!
* Easy web-API to control the robot from your own application.
* API provides both "tank track" style (Y-Y) and joystick style (X-Y) interface.
* Robot stops automatically when connection is lost.

## Requirements
* STS-Pi with Raspberry Pi and Explorer Hat Pro
* Computer / Tablet / Phone with web browser that supports MJPEG
* Tested with the following browsers:  
Linux and Windows: Firefox, Chrome and Opera.  
Android (5.1 on Fairphone 2): Lightning, IceCat Mobile, Chromium.  
CAVEAT: MS Edge and Internet Explorer do not support MJPEG natively.  
Apple Safari and iOS browsers have limited or broken MJPEG support.  
Please use one of the tested browsers instead.

## Install Dependencies
### Picamera
sudo apt-get install python-picamera
### Flask
sudo pip install -U flask
### Gevent
sudo pip install -U gevent
### Explorer Hat
follow these instructions: https://github.com/pimoroni/explorer-hat

## Install STS-PiLot
Clone or download the application into a directory of your choice:
git clone https://github.com/mark-orion/STS-PiLot.git

## Running the program (as normal user, no "sudo" required)  
cd STS-PiLot  
python app.py  

## Start the program automatically while booting
cd STS-Pilot  
chmod +x autostart.sh  
open /etc/rc.local with your preferred editor and add the following line BEFORE the last line reading "exit 0":  
/home/pi/STS-PiLot/autostart.sh  
You may have to change the path if you have saved STS-PiLot at another location.  
Restart the STS-Pi and test if program starts at boot:  
The green LED will flash quickly for about 1 second to indicate STS-PiLot has started.

## Using STS-PiLot
The web interface runs on port 5000 of the Raspberry Pi. You can access it via http://ip_goes_here:5000 or at http://hostname.local:5000 if you have Avahi / mDNS running on your Pi and the client. Hostname is the hostname of your STS-Pi that can be changed with raspi-config (advanced settings).  
Using the webinterface if fairly easy:  
At the center you have the live video with the controls for the two motors to the left and to the right.  
Tapping / clicking on the motor controls sets the forward or reverse speed of the motor.  
For ease of use you can double click / tap and this will set the speed for both motors simultaneously. A single tap / click in the center (video) area of the screen will immediately stop the motors - emergency stop!  
The coloured tiles numbered 1-4 at the bottom of the screen control the corrosponding touchpads / LEDs on the Explorer Hat.  
Touching pad 3 (red) on the screen or the physical device immobilizes the device by toggling the "chocks".  

## Shut down the STS-Pi
The STS-Pi can be shut down completely by activating the "chocks" (red LED flashing) and then pad 4 (green LED flashing). The shutdown will happen after a few seconds and can be interrupted by releasing the chocks (touching pad 3 again).  
At the moment the pads 1 and 2 are not doing anything apart from toggling their LEDs.  

## Web API / URLs to control the robot
### URL example for "half speed forward": http://192.168.1.17:5000/motor?l=50&r=50
### /motor?l=[speed]&r=[speed]
Set speed for the motors (l=left, r=right). Usable values: -100 (full reverse) to 0 (stop) to 100 (full forward)
### /joystick?x=[xaxis]&y=[yaxis]
Two axis interface for the motors. Usable values: -100 (full left/down) to 0 (center) to 100 (full right/up)
### /heartbeat
Resets watchdog timer. All systems stop (chocks_on) if not called every 10 seconds (default setting)
### /touchpad?pad=[1-4]
Toggles Explorer Hat touchpads 1-4 and LEDs
### /video_feed
No frills, bells and whistles MJPEG video feed from the camera
### /
The root serves the web interface itself  

Enjoy! Mark Dammer, Forres, Scotland 2017
