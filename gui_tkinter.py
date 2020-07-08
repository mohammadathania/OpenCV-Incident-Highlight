from tkinter import *
import tkinter as tk
from tkinter import filedialog,Text
from PIL import Image, ImageTk
import cv2
import numpy as np
import pytesseract 
from pytesseract import Output
pytesseract.pytesseract.tesseract_cmd ='\Tesseract.exe'


root=tk.Tk()
root.title('OBJECT TRACKING')
open_video = np.zeros((), np.uint8)
canvas=tk.Canvas(root,height=700,width=500,bg= "#011144")
canvas.pack()
frame=tk.Frame(root,bg="#00FFA4")
frame.place(relwidth=0.8,relheight=0.8,relx=0.1,rely=0.14)



def open_video():
    filename = filedialog.askopenfilename(initialdir = 'Desktop\Github\OpenCV-Incident-Highlight',title = 'Select an Image',filetypes = (('JPG','*.jpg'),('All files','*.*')))
    print(filename)
    global open_video
    open_video = cv2.imread(filename)
    cv2.imshow('frame',open_video)
    cv2.waitKey(0)


def Close_All_Windows():
    cv2.destroyAllWindows()


open_video_btn = tk.Button(canvas,text = 'Open Video', fg = "black",padx = 5,pady = 5, command = open_video)
open_video_btn.place(relx=0.1,rely=0.08)

Close_All_Windows_btn = tk.Button(canvas, text = 'Close All Windows', padx = 5, pady = 5, command = Close_All_Windows)
Close_All_Windows_btn.place(relx = 0.644, rely = 0.08)

root.mainloop()