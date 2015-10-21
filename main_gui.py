__author__ = 'fukszdomonkos'

from tkinter import *
from tkinter import ttk
import threading

from myeps import get_myeps_data, save, LoginError, ParseError

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

        self.export_to_json = IntVar()
        Checkbutton(self.mainframe, text="Export to JSON", variable=self.export_to_json).grid(column=1, row=3,
                                                                                              columnspan=2)
        self.export_to_xlsx = IntVar()
        Checkbutton(self.mainframe, text="Export to Excel", variable=self.export_to_xlsx).grid(column=1, row=4,
                                                                                               columnspan=2)
        self.export_to_html = IntVar()
        Checkbutton(self.mainframe, text="Export to HTML", variable=self.export_to_html).grid(column=1, row=5,
                                                                                              columnspan=2)

        ttk.Button(self.mainframe, text="Save myeps stats", command=self.get_data).grid(column=1, row=6, columnspan=2)
        ttk.Label(self.mainframe, textvariable=self.status).grid(column=1, row=7, columnspan=2)

        for child in self.mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

        username_entry.focus()

    def get_data(self, *args):
        self.status.set("Please wait")
        threading.Thread(target=self.get_data_thread).start()

    def get_data_thread(self):
        export_to_json = True if self.export_to_json.get() == 1 else False
        export_to_xlsx = True if self.export_to_xlsx.get() == 1 else False
        export_to_html = True if self.export_to_html.get() == 1 else False
        if export_to_json or export_to_xlsx or export_to_html:
            try:
                all_data = get_myeps_data(self.username.get(), self.password.get())
                save(all_data, self.username.get(), to_json=export_to_json, to_xlsx=export_to_xlsx,
                     to_html=export_to_html)
                self.status.set("Done")
            except LoginError:  # TODO return specific error messages with LoginError
                self.status.set("Wrong username/password")
        else:
            self.status.set("Choose at least one export format")


root = Tk()
root.title("Myepisodes stat saver")

app = Application(root)

root.mainloop()
