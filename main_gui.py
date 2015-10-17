__author__ = 'fukszdomonkos'

from tkinter import *
from tkinter import ttk
import threading

from myeps import get_myeps_data, save_to_file, LoginError


class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.create_widgets()
        master.bind('<Return>', self.get_data)

    def create_widgets(self):
        self.username = StringVar()
        self.password = StringVar()
        self.status = StringVar()

        ttk.Label(self.mainframe, text="Username:").grid(column=1, row=1, sticky=E)
        username_entry = ttk.Entry(self.mainframe, width=20, textvariable=self.username)
        username_entry.grid(column=2, row=1, sticky=W)

        ttk.Label(self.mainframe, text="Password:").grid(column=1, row=2, sticky=E)
        password_entry = ttk.Entry(self.mainframe, width=20, textvariable=self.password, show='*')
        password_entry.grid(column=2, row=2, sticky=W)

        ttk.Button(self.mainframe, text="Save myeps stats", command=self.get_data).grid(column=1, row=3, columnspan=2)
        ttk.Label(self.mainframe, textvariable=self.status).grid(column=1, row=4, columnspan=2)

        for child in self.mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

        username_entry.focus()

    def get_data(self, *args):
        self.status.set("Please wait")
        threading.Thread(target=self.get_data_thread).start()

    def get_data_thread(self):
        try:
            all_data = get_myeps_data(self.username.get(), self.password.get())
            save_to_file(all_data, self.username.get())
            self.status.set("Done")
        except LoginError:
            self.status.set("Wrong username/password")


root = Tk()
root.title("Myepisodes stat saver")

app = Application(root)

root.mainloop()
