#!/bin/bash
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


