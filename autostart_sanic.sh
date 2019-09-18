#!/bin/bash
# Start UV4L videostream manually
# Comment the following lines out if you use the standard UV4l-raspicam start via systemctl.
# This manual startup method avoids unwanted text overlays on the video output.
# Rotate camera videofeed
v4l2-ctl --set-ctrl horizontal_flip=1
v4l2-ctl --set-ctrl vertical_flip=1
# Start UV4L video streaming
uv4l --external-driver --device-name=video0 &

# Start the STS-Pilot app
#
# Autodetect username
USER=$(stat -c '%U' $0)
# Uncomment following line to manually configure username
#USER="yourname"
# Absolute path to this script.
SCRIPT=$(readlink -f $0)
# Absolute path this script is in.
SCRIPTPATH=$(dirname $SCRIPT)
cd $SCRIPTPATH
su -c "python3 $SCRIPTPATH/app_sanic.py >/dev/null 2>&1 &" $USER 


