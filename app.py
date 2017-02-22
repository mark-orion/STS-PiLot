#!/usr/bin/env python
import os
import sys
import signal
import explorerhat as xhat
import threading
import time
import json
from flask import Flask, request, Response
from gevent.wsgi import WSGIServer

# Raspberry Pi camera module (requires picamera package)
from camera_pi import Camera, check_camera

app = Flask(__name__, static_url_path='/static')
camera_detected = True
brakes = False
chocks = False
blue = False
yellow = False
watchdog_active = True
watchdog_running = True
watchdog = 20
timeout = 10
left_motor = 0
right_motor = 0

# Immobilizes sytem (chocks on) after 'timeout' seconds 
def watchdog_timer():
    global watchdog
    while watchdog_active:
        time.sleep(1)
        if watchdog_running:
            watchdog += 1
            if watchdog > timeout and not chocks:
                chocks_on()
            if watchdog <= timeout and chocks:
                chocks_off()

# Handler for a clean shutdown when pressing Ctrl-C
def signal_handler(signal, frame):
    xhat.light.blue.blink(0.1)
    global watchdog_active
    watchdog_active = False
    brakes_on()
    wd.join()
    http_server.close()
    xhat.light.blue.off()
    sys.exit(0)

# Handler for explorer-hat touchpads
def touch_handler(channel, event):
    global chocks
    global blue
    global yellow
    global watchdog_running
    if channel == 1:
        blue = not blue
        if blue:
            xhat.light.blue.on()
        else:
            xhat.light.blue.off()
    if channel == 2:
        yellow = not yellow
        if yellow:
            xhat.light.yellow.on()
        else:
            xhat.light.yellow.off()
    if channel == 3:
        chocks = not chocks
        if chocks:
            watchdog_running = False;
            chocks_on()
        else:
            watchdog_running = True;
            chocks_off()
    if channel == 4:
        xhat.light.green.blink(0.1)
        time.sleep(5)
        if chocks:
            xhat.light.green.on()
            os.system("sudo -s shutdown -h now")
        else:
            xhat.light.green.off()
    
def brakes_on():
    global brakes
    global left_motor
    global right_motor
    brakes = True
    left_motor = 0;
    right_motor = 0;
    xhat.motor.one.speed(right_motor)
    xhat.motor.two.speed(left_motor)
    
def brakes_off():
    global brakes
    global watchdog
    brakes = False
    watchdog = 0
    
def chocks_on():
    global chocks
    chocks = True
    brakes_on()
    xhat.light.red.blink(0.2)
    
def chocks_off():
    global chocks
    chocks = False
    brakes_off()
    xhat.light.red.off()


# Base URL / - loads web interface        
@app.route('/')
def index():
    return app.send_static_file('index.html')

def gen(camera):
    """Video streaming generator function."""
    if camera_detected:
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    else:
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + '' + b'\r\n')

# URL to remote control touchpads 1-4 on explorer-hat
@app.route('/touchpad')
def touchpad():
    pad = request.args.get('pad')
    if pad:
        touch_handler(int(pad), True)
    return 'ok'

# URL for heartbeat requests (resets watchdog timer)    
@app.route('/heartbeat')
def heartbeat():
    global watchdog
    watchdog = 0
    output = {}
    output['v'] = camera_detected
    output['l'] = left_motor
    output['r'] = right_motor
    output['i1'] = xhat.input.one.read()
    output['i2'] = xhat.input.two.read()
    output['i3'] = xhat.input.three.read()
    output['i4'] = xhat.input.four.read()
    output['a1'] = xhat.analog.one.read()
    output['a2'] = xhat.analog.two.read()
    output['a3'] = xhat.analog.three.read()
    output['a4'] = xhat.analog.four.read()
    return json.dumps(output)

# URL for motor control - format: /motor?l=[speed]&r=[speed]
@app.route('/motor')
def motor():
    global left_motor
    global right_motor
    left = request.args.get('l')
    right = request.args.get('r')
    if left and not chocks:
        left = int(left)
        if left >= -100 and left <= 100:
            left_motor = left
            xhat.motor.two.speed(left_motor)
    if right and not chocks:
        right = int(right)
        if right >= -100 and right <= 100:
            right_motor = right
            xhat.motor.one.speed(right_motor)
    return 'ok'

# URL for joystick input - format: /joystick?x=[x-axis]&y=[y-axis]
@app.route('/joystick')
def joystick():
    global left_motor
    global right_motor
    x_axis = -1 * int(request.args.get('x'))
    y_axis = int(request.args.get('y'))
    x_axis = max( min(x_axis, 100), -100)
    y_axis = max( min(y_axis, 100), -100)
    v = (100-abs(x_axis)) * (y_axis/100) + y_axis
    w = (100-abs(y_axis)) * (x_axis/100) + x_axis
    r = int((v+w) / 2)
    l = int((v-w) / 2)
    if not chocks:
        right_motor = r
        left_motor = l
        xhat.motor.one.speed(right_motor)
        xhat.motor.two.speed(left_motor)
    return 'ok'

# URL for live video feed
@app.route('/video_feed')
def video_feed():
    if camera_detected:
        """Video streaming route. Put this in the src attribute of an img tag."""
        return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return 'no video'

if __name__ == '__main__':
    xhat.light.green.blink(0.1)
    time.sleep(1)
    xhat.light.green.off()
    camera_detected = check_camera()
    
    # register signal handler for a clean exit    
    signal.signal(signal.SIGINT, signal_handler)

    # register handler for touchpads
    xhat.touch.released(touch_handler)
        
    # prepare and start watchdog
    wd = threading.Thread(name='watchdog_timer', target=watchdog_timer)
    wd.start()
    
    #app.run(host='0.0.0.0', debug=False, threaded=True)
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
