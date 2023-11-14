import numpy as np
import cv2
from mss import mss
from PIL import Image
from requests import request
import time
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

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

status("Starting host...")
res = request("POST", BASEURL+"reg/"+name)
if not res.ok:
    status("Could not start. Exiting in 3")
    time.sleep(3)
    exit(-1)
status("Hosting as '"+name+"'")

isQuit = False

def on_closing():
    global isQuit
    btnSubmit['state'] = DISABLED
    isQuit = True
    root.destroy()

btnSubmit['text'] = "Stop"
btnSubmit.configure(text="Stop", command=on_closing)
btnSubmit['state'] = NORMAL

root.protocol("WM_DELETE_WINDOW", on_closing)

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
    cv2.imshow('screen', res)

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break