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
* Robot stops automatically when connection is lost.

## Install Dependencies
### Flask
sudo pip install -U flask
### Gevent
sudo pip install -U gevent
### Explorer Hat
follow the instructions here: https://github.com/pimoroni/explorer-hat

## Install STS-PiLot

