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
from tkinter.ttk import Combobox 
import tkinter as tk


# load our serialized model from disk
import Room



class App(Frame):
	
	def camera(self):
		newWindow = tk.Toplevel(self.master)
		newWindow["bg"] = "gray22"
		labelExample = tk.Label(newWindow, text = "Выберети комнату", fg="green yellow", bg="gray22", font=("Arial", 12)).grid(column=0, row=0)  
		combobox = Combobox(newWindow, values= [1, 2, 3], state='readonly')
		combobox.current(1)
		combobox.grid(column=0, row=2)
		buttonExample = tk.Button(newWindow, text = "Сохранить", fg="green yellow", bg="gray22", font=("Arial", 12)).grid(column=2, row=2)

	def new_camera(self):
		newWindow = tk.Toplevel(self.master)
		newWindow["bg"] = "gray22"
		ip = tk.Label(newWindow, text = "IP Комнаты:", fg="green yellow", bg="gray22", font=("Arial", 12)).grid(column=0, row=0)
		ip_v = tk.Entry(newWindow).grid(column=2, row=0)
		name_room = tk.Label(newWindow, text = "Название комнаты:", fg="green yellow", bg="gray22", font=("Arial", 12)).grid(column=0, row=2)
		name_room_v = tk.Entry(newWindow).grid(column=2, row=2)
		buttonExample2 = tk.Button(newWindow, text = "Сохранить", fg="green yellow", bg="gray22", font=("Arial", 12)).grid(column=1, row=4)

	def __init__(self):
		self.master = Tk()
		self.master.wm_title("HAICV")
		self.master["bg"] = "gray22"
		Frame.__init__(self, self.master)
		self.label = Label(text="", fg="green yellow", bg="gray22", font=("Arial", 14))
		self.label.grid(row = 0, column=11, padx=0, pady=2)
		self.update_clock()
		Label(text="Зашло:", fg="green yellow", bg="gray22", font=("Arial", 14)) \
			.grid(row=0, column=0, padx=0, pady=2)
		self.up = Label(text="0", fg="green yellow", bg="gray22", font=("Arial", 14))
		self.up.grid(row=0, column=1, padx=0, pady=2)
		Label(text="Вышло:", fg="green yellow", bg="gray22", font=("Arial", 14)) \
			.grid(row=0, column=2, padx=0, pady=2)
		self.down = Label(text="0", fg="green yellow", bg="gray22", font=("Arial", 14))
		self.down.grid(row=0, column=3, padx=0, pady=2)
		
		

		self.cam = Button(text="Выбрать камеру", fg="green yellow", bg="gray22", font=("Arial", 9), command=self.camera).grid(row=0, column=6)
		self.newcam = Button(text="Добавить камеру", fg="green yellow", bg="gray22", font=("Arial", 9), command=self.new_camera).grid(row=0, column=8)
		imageFrame = Frame(self.master, width=602, height=600, bg="gray22",)
		imageFrame.grid(row=2, column=0, columnspan=12, padx=10, pady=2)
		self.lmain = Label(imageFrame)
		self.lmain.grid(row=0, column=0)
		self.cap = cv2.VideoCapture(0)
		
		
		
		self.r = Room.Room(self.master)
		self.r.loop()
		self.show_frame()
		self.master.mainloop()
	
	
    	

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
		self.master.after(25, self.show_frame)


#Set up GUI


app=App()




