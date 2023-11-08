import numpy as np
import cv2
from mss import mss
from PIL import Image
# from screeninfo import get_monitors

bounding_box = {'top': 0, 'left': 0, 'width': 400, 'height': 300}
# m1 = get_monitors()[0]

sct = mss()
while True:
    sct_img = sct.grab(sct.monitors[0])
    matlik = np.array(sct_img)
    print(len(matlik))
    # matlik = cv2.resize(matlik, dsize=(int(m1.width/16), int(m1.height/16)))
    res = cv2.resize(matlik, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
    cv2.imshow('screen', res)

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break