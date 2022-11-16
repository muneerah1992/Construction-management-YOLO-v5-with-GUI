import cv2 
from imutils.video import VideoStream
from detect import *
from gui import *



vs = VideoStream(src=0).start()

gui_window = GUI_YOLO(vs)
gui_window.root.mainloop()