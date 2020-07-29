from skimage.measure import compare_ssim as ssim
import matplotlib.pyplot as plt
import cv2
import urllib
import urllib.parse
import urllib.error
import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
import os
from tkinter import filedialog
import sqlite3
import numpy as np
import shutil
from glob import glob
import random
from twilio.rest import Client


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Calibri', size=18, weight="bold")
        self.wm_iconbitmap('icons/icon.ico')
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.geometry("700x500+600+200")
        self.title('IRIS - Interface')

        self.frames = {}
        for F in (LoginPage, Home, Methods):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to IRIS UI",
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        username = ""
        password = ""
        username_entry = Entry(self)
        username_entry.pack()
        password_entry = Entry(self, show='*')
        password_entry.pack()

        def trylogin():
            if username == username_entry.get() and password == password_entry.get():
                controller.show_frame("Home")
            else:
                print("Wrong")

        button = tk.Button(self, text="Log In", command=trylogin)
        button.pack()


class Home(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="IRIS - Home", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        url1 = tk.StringVar()

        def urlimages():
            firstimage = url1.get()
            resource = urllib.urlopen(firstimage)
            output = open("1.png", "wb")
            output.write(resource.read())
            output.close()

        label = tk.Label(self, text="Input Image:")
        label.pack()
        tk.Entry(self, textvariable=url1).pack()

        submit = tk.Button(self, text='Save image', command=urlimages)
        submit.pack()

        def fileDialog():
            try:
                delete = "del 1.png"
                os.system(delete)
                file = filedialog.askopenfilename(initialdir=os.getcwd(), title='Choose a file', filetype=(
                    ("png", "*.png"), ("jpeg", "*.jpg"), ('All Files', "*.*")))
                filedir = r"%s" % file
                shutil.move(filedir, os.getcwd())
                filename = glob('*.png')[0]
                os.rename(file, "1.png")
            except:
                delete = "del 1.png"
                os.system(delete)
                print("Renaming already existing png file")
                filename = glob('*.png')[0]
                os.rename(filename, "1.png")

        label4 = tk.Label(self, text="\n\n")
        label4.pack()

        button = tk.Button(self, text='Browse images', command=fileDialog)
        button.pack()

        label4 = tk.Label(self, text="\n\n")
        label4.pack()

        next = tk.Button(self, text="Continue...",
                         command=lambda: controller.show_frame("Methods"))
        next.pack()


class Methods(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="IRIS - Methods",
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)


        def SSIM():
            img1 = cv2.imread("1.png")
            img11 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            imageA = cv2.resize(img11, (450, 237))
            database = os.listdir("db")
            userData = open('UsersData.txt','r')
            data = userData.read().split('\n')
            count = 0
            result = 0
            imageNumber = 0
            for image in database:

                if(count == 5):
                    break
                count = count + 1
                img2 = cv2.imread("db/" + image)
                imgprocess = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
                imageB = cv2.resize(imgprocess, (450, 237))
                s = ssim(imageA, imageB)

                print('Comparing input image to ' + image + " using MSE")
                title = "Comparing"
                if s < 0:
                    s = 0

                result1 = s * 100
                if result < result1:
                    result = result1
                    imageNumber = count
            print("result is ", result)

            phNo = data[imageNumber-1].split()[-1]
            for root, dirs, files in os.walk("db"):
                if str(imageNumber)+".png" in files:
                    path = os.path.join(root, str(imageNumber)+".png")

            if result < 75:
                label4 = tk.Label(self, text="Iris Not matched please try again or try to contact bank\n")
                label4.pack()
                
            else:
                label4 = tk.Label(self, text="Iris matched, check your mobile for notification\n")
                label4.pack()
                account_sid = 'AC8517ab715c59fb3fc810a2af537b2a85'
                auth_token = '9a8e78279d629faffc34687127c51a4b'

                client = Client(account_sid, auth_token)

                ''' Change the value of 'from' with the number 
                received from Twilio and the value of 'to' 
                with the number in which you want to send message.'''
                message = client.messages.create(
                    from_='+13392176905',
                    body='Dear customer to complete your transaction please click on this link http://websitemine2112.000webhostapp.com/index.html',
                    to=phNo
                )

        def goback():
            controller.show_frame("Home")

        methodssim = tk.Button(
            self, text="click here to validate", command=SSIM)
        methodssim.pack()

        label4 = tk.Label(self, text="\n\n\n")
        label4.pack()

        back = tk.Button(self, text="Go back", command=goback)
        back.pack()


if __name__ == "__main__":
    try:
        remove = "del 1.png"
        os.system(remove)
        app = SampleApp()
        app.mainloop()
    finally:
        remove = "del 1.png"
        os.system(remove)
