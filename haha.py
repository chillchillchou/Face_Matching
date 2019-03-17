import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.input_name = tk.Entry(self)
        self.input_name.pack(side="top")
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "click me"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="bottom")

    def say_hi(self):
        print("hi there, " + str(self.input_name.get()))

root = tk.Tk()
app = Application(master=root)
app.mainloop()

