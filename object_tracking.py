from tkinter import *
import tkinter as tk
from tkinter import filedialog,Text
from PIL import Image,ImageTk
import cv2
import numpy as np
import pytesseract 
from pytesseract import Output
pytesseract.pytesseract.tesseract_cmd ='C:\Program Files\Tesseract OCR\\Tesseract.exe'


root=tk.Tk()
root.title('OBJECT TRACKING')
open_video = np.zeros((), np.uint8)
canvas=tk.Canvas(root,height=700,width=700,bg='blue')
canvas.pack()
frame=tk.Frame(root,bg='yellow')
frame.place(relwidth=0.6,relheight=0.8,relx=0.2,rely=0.05)



def open_video():
    filename = filedialog.askopenfilename(initialdir = 'C:\Git\Image_Processing_Meghashyam\MINI PROJECT',title = 'Select an Image',filetypes = (('JPG','*.jpg'),('All files','*.*')))
    print(filename)
    global open_video
    open_video = cv2.imread(filename)
    cv2.imshow('frame',open_video)
    cv2.waitKey(0)


def Close_All_Windows():
    cv2.destroyAllWindows()


open_video_btn = tk.Button(canvas,text = 'Open Video',fg = 'black',padx = 5,pady = 5, command = open_video)
open_video_btn.place(relx=0.04,rely=0.1)

Close_All_Windows_btn = tk.Button (canvas, text = 'Close All Windows', padx = 10, pady = 10, command = Close_All_Windows)
Close_All_Windows_btn.place (relx = 0.8, rely = 0.9)

root.mainloop()