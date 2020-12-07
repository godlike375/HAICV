# USAGE
# To read and write back out to video:
# python people_counter.py --prototxt mobilenet_ssd/MobileNetSSD_deploy.prototxt \
#	--model mobilenet_ssd/MobileNetSSD_deploy.caffemodel --input videos/example_01.mp4 \
#	--output output/output_01.avi
#
# To read from webcam and write back out to disk:
# python people_counter.py --prototxt mobilenet_ssd/MobileNetSSD_deploy.prototxt \
#	--model mobilenet_ssd/MobileNetSSD_deploy.caffemodel \
#	--output output/webcam_output.avi

# import the necessary packages

import time
import cv2





from tkinter import *
from PIL import Image, ImageTk



# load our serialized model from disk
import Room



class App(Frame):
	def __init__(self,master=None):
		Frame.__init__(self, master)
		self.master = master
		self.label = Label(text="", fg="black", font=("Gotham", 14))
		self.label.grid(row = 0, column=11, padx=0, pady=2)
		self.update_clock()
		Label(text="Зашло:", fg="black", font=("Gotham", 14)) \
			.grid(row=0, column=0, padx=0, pady=2)
		self.up = Label(text="0", fg="black", font=("Gotham", 14))
		self.up.grid(row=0, column=1, padx=0, pady=2)
		Label(text="Вышло:", fg="black", font=("Gotham", 14)) \
			.grid(row=0, column=2, padx=0, pady=2)
		self.down = Label(text="0", fg="black", font=("Gotham", 14))
		self.down.grid(row=0, column=3, padx=0, pady=2)
		Label(text="IP:", fg="black", font=("Gotham", 14)) \
			.grid(row=0, column=4, padx=0, pady=2)
		Entry(width=30, font=("Gotham", 10)) \
			.grid(row=0, column=5, columnspan=3)
		Button(text="Отправить", font=("Gotham", 9)).grid(row=0, column=10)
		imageFrame = Frame(master, width=602, height=600)
		imageFrame.grid(row=2, column=0, columnspan=12, padx=10, pady=2)
		self.lmain = Label(imageFrame)
		self.lmain.grid(row=0, column=0)
		self.cap = cv2.VideoCapture(0)

		self.r = Room.Room()
		self.r.loop()
		self.show_frame()


	def update_clock(self):
		now = time.strftime("%H:%M")
		self.label.configure(text=now)
		self.after(1000, self.update_clock)

	def show_frame(self):
		img = Image.fromarray(self.r.videoframe)
		imgtk = ImageTk.PhotoImage(image=img)
		self.lmain.imgtk = imgtk
		self.lmain.configure(image=imgtk)
		self.up.configure(text=self.r.totalUp)
		self.down.configure(text=self.r.totalDown)
		Room.root.after(25, self.show_frame)


#Set up GUI

app=App(Room.root)



Room.root.mainloop()

del app.r