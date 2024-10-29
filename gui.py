import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import ping_logic
import theme
from ping_logic import get_ssid

class Toplevel1:
    def __init__(self, top=None):
        self.root = top
        self.current_server = "google.com"
        top.geometry("600x570")
        top.title("Ping Tester")


        top.minsize(width=600, height=550)

        self.create_widgets(top)
        
        self.init_graph()

        self.apply_default_theme()

        self.start_ping_monitor()

    def apply_default_theme(self):
        theme.set_auto_mode(root, self.canvas, self.frame, self.ax, self.fig, self.network_label)
        self.combobox.set("Default")

    def create_widgets(self, top):
        # GUI
        self.frame = tk.Frame(top)
        self.frame.place(relx=0, rely=0.20, relwidth=1, relheight=0.75)

        self.canvas = tk.Canvas(top, height=75, width=125, highlightthickness=0)
        self.canvas.place(relx=0.25, rely=0.02, relwidth=0.5, relheight=0.125)

        # Connection name
        self.network_label = tk.Label(top, text=f"Connected: {get_ssid()}", font=("Segoe UI", 10))
        self.network_label.place(relx=0.05, rely=0.02)

        # Combobox theme
        self.combobox = ttk.Combobox(top, values=["Default", "Light", "Dark"], state="readonly", font=("Segoe UI", 9))
        self.combobox.place(relx=0.830, rely=0, relwidth=0.170, relheight=0.058)
        self.combobox.bind("<<ComboboxSelected>>", self.change_mode)

        # Ping server (default = google.com)
        self.server_label = tk.Label(top, text="Server:", font=("Segoe UI", 10))
        self.server_label.place(relx=0.05, rely=0.1)
        self.server_entry = tk.Entry(top, font=("Segoe UI", 10))
        self.server_entry.insert(0, "google.com")  # Domyślna wartość
        self.server_entry.place(relx=0.13, rely=0.1, relwidth=0.3, relheight=0.041)

        # Apply Button
        self.apply_button = tk.Button(top, text="Apply", command=self.apply_server)
        self.apply_button.place(relx=0.46, rely=0.095)

        # Ping space
        self.interval_label = tk.Label(top, text="Space time (s):", font=("Segoe UI", 10))
        self.interval_label.place(relx=0.05, rely=0.15)
        self.interval_spinbox = tk.Spinbox(top, from_=1, to=60, font=("Segoe UI", 10), state="readonly")
        self.interval_spinbox.place(relx=0.205, rely=0.15, relwidth=0.05, relheight=0.042)

    def init_graph(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas_graph = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas_graph.get_tk_widget().pack()
        
    def start_ping_monitor(self):
        interval = int(self.interval_spinbox.get()) * 1000
        ping_logic.check_connection(self.root, self.canvas, self.ax, self.fig, self.current_server)
        self.root.after(interval, self.start_ping_monitor)


    def change_mode(self, event):
        mode = self.combobox.get()
        if mode == "Light":
            theme.set_light_mode(root, self.canvas, self.frame, self.ax, self.fig, self.network_label)
        elif mode == "Dark":
            theme.set_dark_mode(root, self.canvas, self.frame, self.ax, self.fig, self.network_label)
        else:
            theme.set_auto_mode(root, self.canvas, self.frame, self.ax, self.fig, self.network_label)

    def update_network_name(self):
        ssid = get_ssid()
        self.network_label.config(text=f"Connected: {ssid}")
        root.after(10000, self.update_network_name)

    def apply_server(self):
        self.current_server = self.server_entry.get()
        print(f"Server changed: {self.current_server}")



def main(*args):
    global root
    root = tk.Tk()
    root.protocol('WM_DELETE_WINDOW', lambda: (root.destroy(), sys.exit(0)))

    global _top1, _w1
    _top1 = root
    _w1 = Toplevel1(_top1)
    root.mainloop()

if __name__ == '__main__':
    main()
