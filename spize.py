import Tkinter as tk
win = tk.Tk()
win.title("My fuuuu window")
win.geometry('1080x600')
win.resizable(0,0)
def showImg(self):
    load = Image.open('a.jpg')
    render = ImageTk.PhotoImage(load)
    img=Label(self,image=render)
    img.image=render
    img.place(x=50,y=50)
def showText(self):
    text=Label(self,text='success')
    text.pack()
showImg(win)
showText(win)
win.mainloop()
