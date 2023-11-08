import numpy as np
import cv2
from mss import mss
from PIL import Image
from requests import request
import time
from tkinter import *
from tkinter.ttk import *

root = Tk()
root.title = "carryover9"
root.geometry('200x150')
varStatus = StringVar()
varEntered = StringVar()
txtStatus = Label(root, textvariable=varStatus)
txtboxSharename = Text(root)

txtStatus.pack(side="top")

def status(txt):
    varStatus.set(txt)

BASEURL = "https://carryover.nerdakus.repl.co/"
status("pinging server...")
request("GET", BASEURL)
txtboxSharename.pack(side="top")
status("enter sharename")
varEntered.wai
res = request("POST", BASEURL+"reg/"+name)
status(res.text)

sct = mss()
while True:
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