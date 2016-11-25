from main import DataLoader
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from tkinter import Tk, Frame, BOTH, RAISED, RIGHT, LEFT, BOTTOM, TOP, Listbox, END
from tkinter.ttk import Style, Button, Label
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
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


class NavigationWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, background="white")
        self.style = Style()
        self.parent = parent
        self.data = DataLoader(use_test_data=False)
        self.setup_buttons()
        self.controller = controller

    # def init_ui(self):
    #     self.parent.title("Simple")
    #     self.style.theme_use("default")
    #     self.pack(fill=BOTH, expand=True)
    #     self.center_window()
    #     self.setup_buttons()

    def center_window(self):
        width = 290
        height = 150

        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()

        x = (screen_width - width) / 2
        y = (screen_height - height) / 2
        self.parent.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def setup_buttons(self):
        docs = sorted(self.data.subjects.values(), key=lambda document: len(document.views), reverse=True)
        listbox = Listbox(self)
        for val, doc in enumerate(docs[:20]):
            text = doc.doc_id[:6] + "... - " + str(len(doc.views))
            # button = Button(self, text=text, command=lambda x=doc: show_histogram(x.get_views_by_country()))
            button = Button(self, text=text, command=lambda: self.controller.show_frame(GraphPage))
            # button.grid(column=0, row=val)
            listbox.insert(END, button)
        listbox.pack


class Controller(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        Tk.wm_title(self, "Document Tracker Analyser")

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.setup_pages(container)

        self.show_frame(NavigationWindow)

    def setup_pages(self, container):
        for F in (NavigationWindow, GraphPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


def main_function():
    root = Tk()
    root.geometry("250x150+300+300")
    app = Controller()
    root.mainloop()


if __name__ == '__main__':
    main_function()

# https://pythonprogramming.net/change-show-new-frame-tkinter/