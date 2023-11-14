import numpy as np
import cv2
from mss import mss
from PIL import Image
from requests import request
import time
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from threading import Thread

root = Tk()
root.title = "carryover9"
root.geometry('200x150')
varStatus = StringVar()
varEntered = IntVar()
varEntered.set(0)
varScreenShow = BooleanVar()
varScreenShow.set(False)
txtStatus = Label(root, textvariable=varStatus)
txtboxSharename = Entry(root, justify="center")
btnSubmit = Button(root, text="Submit", command=lambda:varEntered.set(varEntered.get()+1))
btnShowScreen = Button(root, text="Show Screen", command=lambda:varScreenShow.set(not varScreenShow.get()))

txtStatus.pack(side="top")

def status(txt):
    varStatus.set(txt)

BASEURL = "https://carryover.nerdakus.repl.co/"
status("Pinging server...")
request("GET", BASEURL)
txtboxSharename.pack(side="top")
btnSubmit.pack(side="top")

def tmp_close():
    varEntered.set(999)
    root.destroy()
root.protocol("WM_DELETE_WINDOW", tmp_close)

status("Enter custom ID")
root.wait_variable(varEntered)
btnSubmit['state'] = DISABLED
name = txtboxSharename.get()

txtboxSharename.delete(0, len(name))
txtboxSharename['show'] = "*"
status("Enter control password")
btnSubmit['state'] = NORMAL
root.wait_variable(varEntered)
btnSubmit['state'] = DISABLED
control = txtboxSharename.get()
txtboxSharename.destroy()

def exitError(txt):
    status(txt)
    time.sleep(3)
    root.destroy()

status("Starting host...")
res = request("POST", BASEURL+"reg/"+name)
if not res.ok:
    Thread(target=exitError, args=["Failed to start. "+str(res.status_code)]).start()
    root.mainloop()
status("Hosting as '"+name+"'")

isQuit = False

def on_closing():
    global isQuit
    btnShowScreen['state'] = DISABLED
    btnSubmit['state'] = DISABLED
    isQuit = True
    root.destroy()

btnSubmit['text'] = "Stop"
btnSubmit.configure(text="Stop", command=on_closing)
btnSubmit['state'] = NORMAL

btnShowScreen.pack(side="top")

root.protocol("WM_DELETE_WINDOW", on_closing)

postSpacing = 0.2

lastPost = time.time()
screenActive = False
sct = mss()
while True:
    if isQuit:
        break
    root.update()
    sct_img = sct.grab(sct.monitors[0])
    matlik = np.array(sct_img)
    # print(len(matlik))
    # matlik = cv2.resize(matlik, dsize=(int(m1.width/16), int(m1.height/16)))
    res = cv2.resize(matlik, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)

    if time.time()-lastPost >= postSpacing:
        request("POST")

    if varScreenShow.get():
        cv2.imshow('screen', res)
        if not screenActive:
            screenActive = True
            btnShowScreen.configure(text="Hide Screen")
    elif screenActive:
        screenActive = False
        cv2.destroyWindow('screen')
        btnShowScreen.configure(text="Show Screen")