from ctypes import alignment
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import imutils
from detect import *
import requests as req

from tkinter import END, Text

class GUI_YOLO:
    def __init__(self, vidStream):
        self.vidStream = vidStream
        self.guiText = ""

        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.stop = False

        # initialize the root window and image panel
        self.root = tki.Tk()
        self.root.configure(bg='black')

        self.panel = None
        self.textbox = None

        # start a thread that constantly pools the video 
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

        # set a callback to handle when the window is closed
        self.root.wm_title("Construction Sites Management")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)


    def get_weather_data(self):
            r = req.get("https://api.openweathermap.org/data/2.5/weather?lat=25.9545400&lon=49.8482480&appid=c284001cdeafab2ff93844fa06e17725&units=metric")
            print(r)
            data = r.json()
            windspeed= round(data['wind']['speed']/1000*3600, 2)
            windgust = round(data['wind']['gust']/1000*3600, 2)
            temperature_val= round(data['main']['temp'] - 273.15, 2)

            weather_data = "Wind Speed = " + str(windspeed) + " km/h \n"
            weather_data += "Wind Gust = " + str(windgust) + " km/h \n"
            weather_data += "Temperature = " + str(temperature_val) + " C \n \n"
            
            return weather_data

    def videoLoop(self):

        # keep looping over frames until we are instructed to stop
        while not self.stopEvent.is_set() and self.stop != True:
            
            # ======================= reading Video frames =======================
            self.frame = self.vidStream.read()
            self.frame = imutils.resize(self.frame, width=300)
            # frame_det = process(self.frame)
            frame_det = run(self.frame)
            # image = cv2.cvtColor(frame_det['frame'], cv2.COLOR_BGR2RGB)
            image = frame_det['frame']
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)

            # ======================= reading API data =======================
            self.guiText += self.get_weather_data()
            self.guiText += "\n\nNo. of workers: " + str(frame_det['workers'][0])



            # ======================= Updating GUI pannels =======================
                    #* Video
            if self.panel is None:
                self.panel = tki.Label(image=image)
                self.panel.image = image
                self.panel.pack(side="left", padx=10, pady=10)
            else:
                self.panel.configure(image=image)
                self.panel.image = image
                    
                    #* API data
            if self.textbox is None:
                self.textbox = Text(self.root, height=10, width=30)
                self.textbox.pack(pady=50)

                self.textbox.insert(END, self.guiText)
            else:
                self.textbox.delete('1.0', END)
                self.textbox.insert(END, self.guiText)
                pass

            self.guiText = ""

            # otherwise, simply update the panel
        print("out of the loop")

    def onClose(self):
		# set the stop event, cleanup the camera, and allow the rest of
		# the quit process to continue
        self.stopEvent.set()
        self.stop = True
        print("[INFO] closing...")
        self.vidStream.stop()
        self.root.quit()


    

