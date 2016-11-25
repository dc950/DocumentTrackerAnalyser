from main import DataLoader
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from tkinter import Tk, Frame, BOTH, RAISED, RIGHT, LEFT, BOTTOM, TOP, Listbox, END
from tkinter import ttk
from tkinter.ttk import Style, Button, Label
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
matplotlib.use("TkAgg")


class GraphPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.document = None
        self.canvas = None
        label = Label(self, text="Graph Page!")
        label.pack(pady=10, padx=10)

        button1 = Button(self, text="Back to Home",
                         command=lambda: self.controller.show_frame(NavigationWindow))
        button1.pack()

    def show_document_data(self, document):
        self.document = document
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()

        self.show_graph(document.get_views_by_country())
        label = Label(self, text="By browser").pack(pady=10, padx=10)
        self.show_graph(document.get_views_by_browser())

    def show_graph(self, data):
        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        width = 0.7
        x, y, labels = self.get_graph_data(data)
        print(labels)
        a.bar(x, y, width)
        a.set_xticks(x + width / 2.0)
        a.set_xticklabels(labels)
        a.autoscale()
        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

    @staticmethod
    def get_graph_data(data):

        x = np.arange(1, len(data) + 1)
        labels, y = [], []
        for label, val in data.items():
            labels.append(label)
            y.append(val)
        return x, y, labels


class NavigationWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.data = DataLoader(use_test_data=False)
        self.controller = controller
        self.active_buttons = []
        self.setup_page()
        self.setup_buttons()

    def setup_page(self):
        label = Label(self, text="Document Tracker Analyser")
        label.grid(column=0, row=0)

    def setup_buttons(self):
        docs = sorted(self.data.subjects.values(), key=lambda document: len(document.views), reverse=True)
        for val, doc in enumerate(docs[:20], 1):
            text = doc.doc_id[:6] + "... "
            button = Button(self, text=text, width=20,
                            command=lambda document=doc: self.controller.show_graph_page(document))
            button.grid(column=0, row=val)
            label = Label(self, text=str(len(doc.views)) + " views")
            label.grid(column=1, row=val)
            self.active_buttons.append((button, label))


class Controller(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        Tk.wm_title(self, "Document Tracker Analyser")
        self.style = Style()
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

    def show_graph_page(self, document):
        frame = self.frames[GraphPage]
        frame.tkraise()
        frame.show_document_data(document)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


def main_function():

    app = Controller()
    app.mainloop()


if __name__ == '__main__':
    main_function()

# https://pythonprogramming.net/change-show-new-frame-tkinter/