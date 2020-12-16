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
import server_connector as sc

from tkinter import *
from PIL import Image, ImageTk
from tkinter.ttk import Combobox
import tkinter as tk
from tkinter import messagebox as mb

# load our serialized model from disk
import Room
import threading


class App(Frame):

    def on_chosen(self, event):
        res = self.combobox.get()
        if(len(res)>0):
            for i in range(len(self.rooms)):
                if self.rooms[i].name == res:
                    self.current_room_number = i
            self.current_room = self.rooms[self.current_room_number]

    def choose_camera(self):
        newWindow = tk.Toplevel(self.master)
        newWindow["bg"] = "gray22"
        labelExample = tk.Label(newWindow, text="Выберите комнату", fg="green yellow", bg="gray22",
                                font=("Arial", 12)).grid(column=0, row=0)
        self.combobox = Combobox(newWindow,
                                 values=[i.name for i in self.rooms] if len(self.rooms) > 0 else [""],
                                 state='readonly')
        self.combobox.current(self.current_room_number)
        self.combobox.grid(column=0, row=2)
        self.combobox.bind("<<ComboboxSelected>>", self.on_chosen)

    def new_camera(self):
        newWindow = tk.Toplevel(self.master)
        self.newWindow = newWindow
        newWindow["bg"] = "gray22"
        ip = tk.Label(newWindow, text="IP Комнаты: (адрес видеофайла)", fg="green yellow", bg="gray22",
                      font=("Arial", 12)).grid(column=0, row=0)
        self.ip_v = tk.Entry(newWindow)
        self.ip_v.insert(0,"videos/")
        self.ip_v.grid(column=1, row=0)
        name_room = tk.Label(newWindow, text="Название комнаты:", fg="green yellow", bg="gray22", font=("Arial", 12))
        name_room.grid(column=0, row=2)
        self.name_room_v = tk.Entry(newWindow)
        self.name_room_v.grid(column=1, row=2)
        buttonExample2 = tk.Button(newWindow, command=self.save_room, text="Сохранить", fg="green yellow", bg="gray22",
                                   font=("Arial", 12)).grid(column=1, row=4)

    def save_room(self):
        if self.name_room_v.get()!="":
            for i in self.rooms:
                if i.name == self.name_room_v.get():
                    mb.showerror(title="error", message="Такое имя уже существует")
                    return 0
        else:
            mb.showerror(title="error", message="имя не может быть пустым")
            return 0
        try:
            f = open(self.ip_v.get())
        except IOError:
            mb.showerror(title="error", message="не удалось открыть файл")
            return 0
        room = Room.Room(self.master, self.ip_v.get(), self.name_room_v.get())

        self.rooms.append(room)
        room.loop()
        # self.current_room = self.rooms[self.current_room_number]
        self.newWindow.destroy()

    def __init__(self):
        self.rooms = []
        self.current_room_number = 0
        self.master = Tk()
        self.master.wm_title("HAICV")
        self.master["bg"] = "gray22"
        Frame.__init__(self, self.master)
        self.label = Label(text="", fg="green yellow", bg="gray22", font=("Arial", 14))
        self.label.grid(row=0, column=11, padx=0, pady=2)
        self.update_clock()
        Label(text="Всего людей:", fg="green yellow", bg="gray22", font=("Arial", 14)) \
            .grid(row=0, column=0, padx=0, pady=2)
        self.total = Label(text="0", fg="green yellow", bg="gray22", font=("Arial", 14))
        self.total.grid(row=0, column=1, padx=0, pady=2)
        # Label(text="Вышло:", fg="green yellow", bg="gray22", font=("Arial", 14)) \
        #    .grid(row=0, column=2, padx=0, pady=2)
        # self.down = Label(text="0", fg="green yellow", bg="gray22", font=("Arial", 14))
        # self.down.grid(row=0, column=3, padx=0, pady=2)

        self.cam = Button(text="Выбрать камеру", fg="green yellow", bg="gray22", font=("Arial", 9),
                          command=self.choose_camera).grid(row=0, column=6)
        self.newcam = Button(text="Добавить камеру", fg="green yellow", bg="gray22", font=("Arial", 9),
                             command=self.new_camera).grid(row=0, column=8)
        imageFrame = Frame(self.master, width=602, height=600, bg="gray22", )
        imageFrame.grid(row=2, column=0, columnspan=12, padx=10, pady=2)
        self.lmain = Label(imageFrame)
        self.lmain.grid(row=0, column=0)

        # self.current_room_number = 0
        # self.current_room = self.rooms[self.current_room_number]
        # self.current_room.loop()
        self.show_frame()
        sc.setup()
        self.send_stats()

        self.master.mainloop()

    def update_clock(self):
        now = time.strftime("%H:%M")
        self.label.configure(text=now)
        self.after(1000, self.update_clock)

    def show_frame(self):
        if (hasattr(self, 'current_room')):
            if (hasattr(self.current_room, 'videoframe')):
                img = Image.fromarray(self.current_room.videoframe)
                imgtk = ImageTk.PhotoImage(image=img)
                self.lmain.imgtk = imgtk
                self.lmain.configure(image=imgtk)
                self.total.configure(text=self.current_room.total)
                # self.down.configure(text=self.current_room.totalDown)

        self.master.after(25, self.show_frame)

    def send_stats(self):
        if (hasattr(self, 'current_room')):
            thread = threading.Thread(target=sc.send_counters, args=(self.rooms,))
            thread.start()
        self.master.after(1000, self.send_stats)


# Set up GUI


app = App()
