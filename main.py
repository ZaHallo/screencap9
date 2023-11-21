import numpy as np
import cv2
from mss import mss
from PIL import Image
import requests
import time
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from threading import Thread
import json
import zlib
import asyncio
import ssl
import os
import websockets

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

BASEURL = "https://bruh2.orangetomato.repl.co/"
BASEHOOKURL = "wss://bruh2.orangetomato.repl.co/"
status("Pinging server...")
req = requests.request("GET", BASEURL)
txtboxSharename.pack(side="top")
btnSubmit.pack(side="top")
root.update()

def on_closing():
    global isQuit
    btnShowScreen['state'] = DISABLED
    btnSubmit['state'] = DISABLED
    isQuit = True
    root.destroy()

def exitError(txt):
    status(txt)
    root.update()
    time.sleep(3)
    root.destroy()
    exit()

    # Thread(target=exitError, args=["Failed to open webhook. "+str(websocket.close_code)+"\n"+str(websocket.close_reason)]).start()

# CERT = ssl.SSLContext()

os.system("clear")

def tmp_close():
    varEntered.set(999)
    root.destroy()

# websocket.enableTrace(True)
async def Main():
    root.protocol("WM_DELETE_WINDOW", tmp_close)

    websocket = await websockets.connect(uri=BASEHOOKURL)
    if websocket.closed:
        exitError("Failed to open webhook. "+str(websocket.close_code)+"\n"+str(websocket.close_reason))

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
    await websocket.send(json.dumps({'type':'start','data':{'name':name,'key':control}}))
    res = await websocket.recv()

    isQuit = False

    loop = asyncio.get_event_loop()

    time.sleep(0.2)
    status("Hosting as '"+name+"'")

    CurrentWebsocketData = []

    btnSubmit['text'] = "Stop"
    btnSubmit.configure(text="Stop", command=on_closing)
    btnSubmit['state'] = NORMAL

    btnShowScreen.pack(side="top")

    root.protocol("WM_DELETE_WINDOW", on_closing)

    postSpacing = 2

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
        res = cv2.resize(matlik, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LANCZOS4)

        if time.time()-lastPost >= postSpacing:
            lastPost = time.time()
            CurrentWebsocketData = res.tolist()
            comp = json.dumps(CurrentWebsocketData)
            comp = zlib.compress(comp.encode())
            try:
                await websocket.send(json.dumps({'type':'update','data':{'name':name,'screen':json.dumps(CurrentWebsocketData)}}))
                await websocket.recv()
            except Exception as e:
                with open("logfile.txt", mode="a") as f:
                    f.write(str(e)+"\n")
                break


        if varScreenShow.get():
            cv2.imshow('screen', res)
            if not screenActive:
                screenActive = True
                btnShowScreen.configure(text="Hide Screen")
        elif screenActive:
            screenActive = False
            cv2.destroyWindow('screen')
            btnShowScreen.configure(text="Show Screen")
    
    root.destroy()
    exit()
# async def WebsocketHandler():
#     print('stg0')
#     while True:
#         print('stg1')
#         global CurrentWebsocketData
#         print('stg2')
#         jsonData = json.dumps({'name':name,'screen':CurrentWebsocketData})
#         await websocket.send("h")
#         print('stg3')
#         data = await websocket.recv()
#         print('stg4')
#         print("DATA GOT???")
#         print(data)

asyncio.run(Main())