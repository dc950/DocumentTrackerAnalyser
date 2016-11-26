from main import DataLoader
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
        self.controller = controller
        self.canvas = None
        label = Label(self, text="Graph Page!")
        label.pack(pady=10, padx=10)

        button1 = Button(self, text="Back to Home",
                         command=lambda: self.controller.show_frame(NavigationWindow))
        button1.pack()

    def show_document_data(self, document):
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()

        self.show_graph(document.get_views_by_country(), "Views by Country")
        self.show_graph(document.get_views_by_browser(), "Views by Browser")

        buttons = []
        also_likes = document.also_likes()
        for doc in also_likes:
            button = Button(self, text=doc.doc_id[:6] + "...",
                            command=lambda the_doc=doc: self.controller.show_graph_page(the_doc))
            buttons.append(button)
            button.pack()

    def show_views_by_browser_global(self, data):
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
        self.show_graph(data, "Global Browser Stats")

    def show_graph(self, data, title):
        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        f.suptitle(title, fontsize=14)
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
        data = self.data.get_views_by_browser_global()
        button = Button(self, text="Global browser stats",
                        command=lambda: self.controller.show_graph_page_browser(data))
        button.grid(column=1, row=0)

    def setup_buttons(self):
        docs = sorted(self.data.subjects.values(), key=lambda document: len(document.views), reverse=True)
        # Setup documents
        for val, doc in enumerate(docs[:20], 1):
            text = doc.doc_id[:6] + "... "
            button = Button(self, text=text, width=20,
                            command=lambda document=doc: self.controller.show_graph_page(document))
            button.grid(column=0, row=val)
            label = Label(self, text=str(len(doc.views)) + " views")
            label.grid(column=1, row=val)
            self.active_buttons.append((button, label))
        # Setup Readers
        readers = sorted(self.data.visitors.values(), key=lambda reader: reader.total_view_time(), reverse=True)
        for val, reader in enumerate(readers[:10], 1):
            text = str(val) + ": " + reader.uuid[:6] + "..."
            label = Label(self, text=text + " " + str(reader.total_view_time()) + " time viewed")
            label.grid(column=3, row=val)


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

    def show_graph_page_browser(self, data):
        frame = self.frames[GraphPage]
        frame.tkraise()
        frame.show_views_by_browser_global(data)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


def main_function():
    app = Controller()
    app.mainloop()


if __name__ == '__main__':
    main_function()
