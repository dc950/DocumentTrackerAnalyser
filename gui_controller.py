import getopt
import sys
from tkinter import Tk, Frame, BOTH, LEFT, TOP
from tkinter.ttk import Style, Button, Label

import matplotlib
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from data_loader import DataLoader

matplotlib.use("TkAgg")


class GraphPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.page_items = []
        label = Label(self, text="Graph Page!")
        label.pack(pady=10, padx=10)
        button1 = Button(self, text="Back to Home",
                         command=lambda: self.controller.show_frame(NavigationWindow))
        button1.pack()

    def show_document_data(self, document, user=None):
        self.clear_page()

        also_likes = document.also_likes(user=user)
        for doc in also_likes:
            button = Button(self, text=doc.doc_id[:6] + "...",
                            command=lambda the_doc=doc: self.controller.show_graph_page(the_doc))
            self.page_items.append(button)
            button.pack(side=TOP, pady=10, padx=10)

        self.show_graph(document.get_views_by_country(), "Views by Country").pack(side=LEFT, fill=BOTH, expand=True)
        self.show_graph(document.get_views_by_continent(), "Views by Continent").pack(side=LEFT, fill=BOTH, expand=True)
        self.show_graph(document.get_views_by_browser(), "Views by Browser").pack(side=LEFT, fill=BOTH, expand=True)

    def show_views_by_browser_global(self, data):
        self.clear_page()
        self.show_graph(data, "Global Browser Stats").pack(side=LEFT, fill=BOTH, expand=True, pady=10)

    def show_graph(self, data, title):
        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        f.suptitle(title, fontsize=14)
        width = 0.7
        x, y, labels = self.get_graph_data(data)
        a.bar(x, y, width)
        a.set_xticks(x + width / 2.0)
        a.set_xticklabels(labels,  rotation=45)
        a.autoscale()
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        # canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
        self.page_items.append(canvas.get_tk_widget())
        return canvas.get_tk_widget()

    @staticmethod
    def get_graph_data(data):
        x = np.arange(1, len(data) + 1)
        labels, y = [], []
        for label, val in data.items():
            labels.append(label)
            y.append(val)
        return x, y, labels

    def clear_page(self):
        for item in self.page_items:
            item.pack_forget()


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
        # data = self.data.get_views_by_browser_global()
        button = Button(self, text="Global browser stats",
                        command=lambda: self.controller.show_graph_page_browser(self.data.get_views_by_browser_global()))
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
        readers = sorted(self.data.visitors.values(), key=lambda r: r.total_view_time(), reverse=True)
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

    def show_graph_page(self, document, user=None):
        frame = self.frames[GraphPage]
        frame.tkraise()
        frame.show_document_data(document, user=user)

    def show_graph_page_browser(self, data):
        frame = self.frames[GraphPage]
        frame.tkraise()
        frame.show_views_by_browser_global(data)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


def start_gui():
    app = Controller()
    app.mainloop()
    return app


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "u:d:t:")
    except getopt.GetoptError:
        print('Incorrect parameter specified')
        sys.exit(2)
    user_id, doc_id, task_id = None, None, 0
    for opt, arg in opts:
        if opt == '-u':
            user_id = arg
        elif opt == '-d':
            doc_id = arg
        elif opt == '-t':
            task_id = int(arg)

    if task_id == 0:
        print("No task specified")
        start_gui()
    elif task_id == 1:
        print("It was made in python.")
    elif task_id == 2:
        requires_error(doc_id is None, "No document id given")
        app = start_gui()
        app.show_graph_page(app.frames[NavigationWindow].data.documents[doc_id])  # TODO better access
    elif task_id == 3:
        app = start_gui()
        app.show_graph_page_browser(app.frames[NavigationWindow].data.get_views_by_browser_global)
    elif task_id == 4:
        data = DataLoader()
        readers = sorted(data.visitors.values(), key=lambda r: r.total_view_time(), reverse=True)
        for val, reader in enumerate(readers[:10], 1):
            print(str(val) + ": " + reader.uuid)
        # start_gui()  # is shown on main page...
    elif task_id == 5:
        requires_error(doc_id is None, "No document id given")
        data_loader = DataLoader()
        data_loader.load_data(False)
        doc = data_loader.subjects[doc_id]
        if user_id is not None:
            user = data_loader.visitors[user_id]
        else:
            user = None
        also_likes = doc.also_likes(user=user)
        if len(also_likes) == 0:
            print("No other likes found")
        for other_doc in also_likes:
            print(also_likes)

    elif task_id == 6:
        start_gui()
    elif task_id == 7:
        print("The command-line works, see")


def requires_error(condition, msg):
    if condition:
        print(msg)
        sys.exit(2)

if __name__ == '__main__':
    main(sys.argv[1:])

