function makeHttpObject() {
    try {return new XMLHttpRequest();}
    catch (error) {}
    try {return new ActiveXObject("Msxml2.XMLHTTP");}
    catch (error) {}
    try {return new ActiveXObject("Microsoft.XMLHTTP");}
    catch (error) {}
    throw new Error("Could not create HTTP request object.");
}
var request = makeHttpObject();
var newSpeedL = 0;
var newSpeedR = 0;
var actSpeedL = 0;
var actSpeedR = 0;
var doubleClick = false;
var inactive = "0px";
var active = "10px solid black";
var clickTimer = setTimeout(reset_doubleclick, 200);
setInterval(heartbeat, 5000);
function heartbeat() {
    var heartbeat_url = "/heartbeat";
    request.open("GET", heartbeat_url, true);
    request.send(null);
}
function reset_doubleclick() {
    doubleClick = false;
}
function set_doubleclick() {
    clearTimeout(clickTimer);
    clickTimer = setTimeout(reset_doubleclick, 200);
    doubleClick = true;
}
function motor_l(lspeed) {
    newSpeedL = lspeed;
    if (lspeed == actSpeedL && lspeed != actSpeedR && doubleClick) {
	newSpeedR = lspeed;
	doubleClick = false;
    } else {
	set_doubleclick();
    }
    set_motor();
}
function motor_r(rspeed) {
    newSpeedR = rspeed;
    if (rspeed == actSpeedR && rspeed != actSpeedL && doubleClick) {
	newSpeedL = rspeed;
	doubleClick = false;
    } else {
	set_doubleclick();
    }
    set_motor();
}
function set_motor() {
    var motor_url = "/motor?l=" + newSpeedL.toString() + '&r=' + newSpeedR.toString();
    request.open("GET", motor_url, true);
    request.send(null);
    var oldId = "l" + actSpeedL.toString();
    var newId = "l" + newSpeedL.toString();
    document.getElementById(oldId).style.outline = inactive;
    document.getElementById(newId).style.outline = active;
    oldId = "r" + actSpeedR.toString();
    newId = "r" + newSpeedR.toString();
    document.getElementById(oldId).style.outline = inactive;
    document.getElementById(newId).style.outline = active;
    actSpeedL = newSpeedL;
    actSpeedR = newSpeedR;
}
function touchpad(pad) {
    var touchpad_url = "/touchpad?pad=" + pad.toString();
    request.open("GET", touchpad_url, true);
    request.send(null);
}
function brake() {
    newSpeedR = 0;
    newSpeedL = 0;
    set_motor();
}   
