from __future__ import print_function
import cv2
import sys

def check_camera():
    return True
    
class Camera(object):

    def __init__(self):
        self.width = 320
        self.height = 240
        self.video_src = 0
        self.loop = False
        self.flip = 1
        self.cam = cv2.VideoCapture(self.video_src)
        self.cam.set(cv.CV_CAP_PROP_FRAME_WIDTH, float(self.input_width))
        self.cam.set(cv.CV_CAP_PROP_FRAME_HEIGHT, float(self.input_height))
        if self.cam is None or not self.cam.isOpened():
            print("Warning: unable to open video source:" + str(self.video_src), file = sys.stderr)


    def get_frame(self):
        self.ret, self.video_frame = self.cam.read()
        while self.ret is False:
            if self.loop:
                self.cam.set(cv.CV_CAP_PROP_POS_FRAMES, 0)
                self.ret, self.video_frame = self.cam.read()
            else:
                self.error_handler()
        self.video_frame = cv2.flip(self.video_frame, self.flip)
        return self.video_frame
    
    def error_handler(self):
        print("No more frames or capture device down - exiting.",
              file=sys.stderr)
        sys.exit(0)

    '''
    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            # camera setup
            cam = cv2.VideoCapture(video_src)
            cam.set(cv.CV_CAP_PROP_FRAME_WIDTH,
                         float(input_width))
            cam.set(cv.CV_CAP_PROP_FRAME_HEIGHT,
                         float(input_height))
            time.sleep(2)

            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # store frame
                stream.seek(0)
                cls.frame = stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

                # if there hasn't been any clients asking for frames in
                # the last 10 seconds stop the thread
                if time.time() - cls.last_access > 10:
                    break
        cls.thread = None
    '''
