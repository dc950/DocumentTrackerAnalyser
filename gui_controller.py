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


def sort_by_views(doc_views):
    return sorted(doc_views, key=lambda doc: doc_views[doc][0], reverse=True)


def sort_by_readtime(doc_views):
    return sorted(doc_views, key=lambda doc: doc_views[doc][1], reverse=True)


class GraphPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.page_items = []

        button1 = Button(self, text="Back to Home",
                         command=lambda: self.controller.show_frame(NavigationWindow))
        button1.pack()

    def show_document_data(self, document, user=None):
        self.clear_page()

        label = Label(self, text="Document: "+document.doc_id)
        label.pack(pady=10, padx=10)
        self.page_items.append(label)
        print(document.doc_id)

        also_likes = document.also_likes(sort_by_views, user=user)
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
    def __init__(self, parent, controller, data):
        Frame.__init__(self, parent, background="white")
        self.parent = parent

        self.controller = controller
        self.active_buttons = []
        self.setup_page(data)
        self.setup_buttons(data)

    def setup_page(self, data):
        label = Label(self, text="Document Tracker Analyser")
        label.grid(column=0, row=0)
        # data = self.data.get_views_by_browser_global()
        button = Button(self, text="Global browser stats",
                        command=lambda: self.controller.show_graph_page_browser(data.get_views_by_browser_global()))
        button.grid(column=1, row=0)

    def setup_buttons(self, data):
        docs = sorted(data.documents.values(), key=lambda document: len(document.views), reverse=True)
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
        readers = sorted(data.visitors.values(), key=lambda r: r.total_view_time(), reverse=True)
        for val, reader in enumerate(readers[:10], 1):
            text = str(val) + ": " + reader.uuid[:6] + "..."
            label = Label(self, text=text + " " + str(reader.total_view_time()) + " time viewed")
            label.grid(column=3, row=val)


class Controller(Tk):
    def __init__(self, task=None, doc_id=None, user_id=None, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        Tk.wm_title(self, "Document Tracker Analyser")
        self.style = Style()
        self.data = DataLoader(use_test_data=False)
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.setup_pages(container)

        self.show_frame(NavigationWindow)

        # TODO enum?
        # TODO try catch doc_id
        if task == '2':
            self.show_graph_page(self.data.documents[doc_id])
        elif task == '3a':
            self.show_graph_page_browser(self.data.get_views_by_browser_global_base())
        elif task == '3b':
            self.show_graph_page_browser(self.data.get_views_by_browser_global())

    def setup_pages(self, container):
        frame = NavigationWindow(container, self, self.data)
        self.frames[NavigationWindow] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        frame = GraphPage(container, self)
        self.frames[GraphPage] = frame
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


def start_gui(task=None, doc_id=None):
    app = Controller(task=task, doc_id=doc_id)
    app.mainloop()
    return app


# TODO move
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "u:d:t:")
    except getopt.GetoptError:
        print('Incorrect parameters specified')
        sys.exit(2)
    user_id, doc_id, task_id = None, None, 0
    for opt, arg in opts:
        if opt == '-u':
            user_id = arg
        elif opt == '-d':
            doc_id = arg
        elif opt == '-t':
            task_id = arg

    if task_id == '2a' or task_id == '2b' or task_id == '2':
        print(task_id)
        requires_error(doc_id is None, "No document id given")
        start_gui(task='2', doc_id=doc_id)
    elif task_id == '3a':
        start_gui(task=task_id)
    elif task_id == '3b':
        start_gui(task=task_id)
    elif task_id == '4':
        data = DataLoader()
        readers = sorted(data.visitors.values(), key=lambda r: r.total_view_time(), reverse=True)
        for val, reader in enumerate(readers[:10], 1):
            print(str(val) + ": " + reader.uuid)
    elif task_id == '5a':
        task_5(sort_by_views, doc_id, user_id)
    elif task_id == '5b':
        task_5(sort_by_readtime, doc_id, user_id)
    else:
        start_gui()


def task_5(sort, doc_id, user_id):
    requires_error(doc_id is None, "No document id given")
    data_loader = DataLoader()
    doc = data_loader.documents[doc_id]
    if user_id is not None:
        user = data_loader.visitors[user_id]
    else:
        user = None
    also_likes = doc.also_likes(sort, user=user)
    if len(also_likes) == 0:
        print("No other likes found")
    for liked_doc in also_likes:
        print(liked_doc.doc_id)


def requires_error(condition, msg):
    if condition:
        print(msg)
        sys.exit(2)

if __name__ == '__main__':
    main(sys.argv[1:])

