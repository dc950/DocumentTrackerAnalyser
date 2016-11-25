import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from tkinter import Tk, Frame, BOTH, RAISED, RIGHT, LEFT, BOTTOM, TOP
from tkinter.ttk import Style, Button, Label
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from gui_controller import NavigationWindow
matplotlib.use("TkAgg")


class GraphPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Graph Page!")
        label.pack(pady=10, padx=10)

        button1 = Button(self, text="Back to Home",
                         command=lambda: controller.show_frame(NavigationWindow))
        button1.pack()
        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

    def show_histogram(self, data):
        print(data)
        x = np.arange(1, len(data) + 1)
        labels, y = [], []
        for label, val in data.items():
            labels.append(label)
            y.append(val)

        width = 0.9
        plt.bar(x, y, 1)
        plt.xticks(x + width / 2.0, labels)
        plt.show()
