from tkinter import *
import pyautogui
import cv2
import datetime,time
import pytesseract
pytesseract.pytesseract.tesseract_cmd=r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

class Application():
    def __init__(self, master):
        self.master = master
        self.rect = None
        self.x = self.y = 0
        self.start_x = None
        self.start_y = None
        self.curX = None
        self.curY = None

        # root.configure(background = 'red')
        # root.attributes("-transparentcolor","red")

        root.attributes("-transparent", "blue")
        root.geometry('400x50+200+200')  # set new geometry
        root.title('Select Area')
        self.menu_frame = Frame(master, bg="blue")
        self.menu_frame.pack(fill=BOTH, expand=YES)

        self.buttonBar = Frame(self.menu_frame,bg="")
        self.buttonBar.pack(fill=BOTH,expand=YES)

        self.snipButton = Button(self.buttonBar, width=20,text="Select Screen Area", command=self.createScreenCanvas, background="green")
        self.snipButton.pack(expand=YES)

        self.master_screen = Toplevel(root)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "blue")
        self.picture_frame = Frame(self.master_screen, background = "blue")
        self.picture_frame.pack(fill=BOTH, expand=YES)
        self.l=Label(root,text="Enter Time In Seconds")
        self.l.pack(side=LEFT)
        self.E1 = Entry(root, bd =5)
        self.E1.pack(side = RIGHT)
    def takeBoundedScreenShot(self, x1, y1, x2, y2):
        im = pyautogui.screenshot(region=(x1, y1, x2, y2))
        x = datetime.datetime.now()
        fileName = x.strftime("%f")
        im.save(fileName + ".png")

    def createScreenCanvas(self):
        self.master_screen.deiconify()
        root.withdraw()

        self.screenCanvas = Canvas(self.picture_frame, cursor="cross", bg="grey11")
        self.screenCanvas.pack(fill=BOTH, expand=YES)

        self.screenCanvas.bind("<ButtonPress-1>", self.on_button_press)
        self.screenCanvas.bind("<B1-Motion>", self.on_move_press)
        self.screenCanvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.master_screen.attributes('-fullscreen', True)
        self.master_screen.attributes('-alpha', .3)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    def on_button_release(self, event):
        self.recPosition()
        global t
        t=self.E1.get()
        global co
        if self.start_x <= self.curX and self.start_y <= self.curY:
            co=[self.start_x, self.start_y, self.curX - self.start_x, self.curY - self.start_y]

        elif self.start_x >= self.curX and self.start_y <= self.curY:
            co=[self.curX, self.start_y, self.start_x - self.curX, self.curY - self.start_y]

        elif self.start_x <= self.curX and self.start_y >= self.curY:
            co=[self.start_x, self.curY, self.curX - self.start_x, self.start_y - self.curY]

        elif self.start_x >= self.curX and self.start_y >= self.curY:
            co=[self.curX, self.curY, self.start_x - self.curX, self.start_y - self.curY]

        self.exitScreenshotMode()
        self.exit_application()
        root.destroy()

    def exitScreenshotMode(self):
        #print("Screenshot mode exited")
        self.screenCanvas.destroy()
        self.master_screen.withdraw()
        root.deiconify()

    def exit_application(self):
        #print("Application exit")
        root.quit()

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.screenCanvas.canvasx(event.x)
        self.start_y = self.screenCanvas.canvasy(event.y)

        self.rect = self.screenCanvas.create_rectangle(self.x, self.y, 1, 1, outline='black', width=3, fill="grey")

    def on_move_press(self, event):
        self.curX, self.curY = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.screenCanvas.coords(self.rect, self.start_x, self.start_y, self.curX, self.curY)

    def recPosition(self):
        print()
        #print(self.start_x)
        #print(self.start_y)
        #print(self.curX)
        #print(self.curY)

if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    root.mainloop()

#print(int(t))
def takeBoundedScreenShot(x1, y1, x2, y2):
    f = open("output.txt", "a")
    i=0
    prevt=' '
    first_time = datetime.datetime.now()
    later_time = datetime.datetime.now()
    while(int((later_time-first_time).total_seconds()) <=int(t)):
        im = pyautogui.screenshot(region=(x1, y1, x2, y2))
        im.save("temp"+ ".png")
        time.sleep(0.5)
        img=cv2.imread('temp.png')
        text=pytesseract.image_to_string(img)
        if(text.find(prevt)!=-1):
            text=text.replace(text[0:text.index(prevt)+len(prevt)],'')
        text.replace('�','')
        prevt=text[-10:]
        f.write(text)
        later_time = datetime.datetime.now()

takeBoundedScreenShot(co[0],co[1],co[2],co[3])
