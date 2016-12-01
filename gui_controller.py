from tkinter import Tk, Frame, BOTH, LEFT, TOP
from tkinter.ttk import Style, Button, Label, Entry

import matplotlib
import numpy as np
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from data_loader import DataLoader

matplotlib.use("TkAgg")


def sort_by_views(doc_views):
    sorted_docs = sorted(doc_views, key=lambda document: doc_views[document][0], reverse=True)
    for doc in sorted_docs:
        yield (doc, doc_views[doc])


def sort_by_readtime(doc_views):
    sorted_docs = sorted(doc_views, key=lambda document: doc_views[document][1], reverse=True)
    for doc in sorted_docs:
        yield (doc, doc_views[doc])


class HeaderFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        button1 = Button(self, text="Back to Home",
                         command=lambda: controller.show_frame(NavigationPage))
        button1.pack(side=TOP)

        self.controller = controller
        self.buttons = []

    def clear(self):
        for button in self.buttons:
            button.pack_forget()
        self.buttons = []

    def display_also_likes(self, doc_id, also_likes):
        self.clear()

        label_header = Label(self, text="Document " + doc_id, font=("Helvetica", 16))
        label_header.pack(side=TOP)
        self.buttons.append(label_header)
        if len(also_likes) > 0:
            also_likes_label = Label(self, text="Users who read this also read")
            also_likes_label.pack(side=LEFT)
            self.buttons.append(also_likes_label)
        for i, doc in enumerate(also_likes):
            button = Button(self, text=doc[0].doc_id[:6] + "...",
                            command=lambda the_doc=doc[0]: self.controller.show_graph_page(the_doc))
            self.buttons.append(button)
            button.pack(side=LEFT)


class GraphPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.frame_header = HeaderFrame(self, controller)
        self.frame_header.pack(side=TOP)
        self.controller = controller
        self.page_items = []

    def show_document_data(self, document, user=None):
        self.clear_page()
        also_likes = document.also_likes(sort=sort_by_views, user=user)
        self.frame_header.display_also_likes(document.doc_id, also_likes)

        self.show_graph(document.views_by_country, "Views by Country").pack(side=LEFT, fill=BOTH, expand=True)
        self.show_graph(document.views_by_continent, "Views by Continent").pack(side=LEFT, fill=BOTH, expand=True)
        self.show_graph(document.views_by_browser, "Views by Browser").pack(side=LEFT, fill=BOTH, expand=True)

    def show_views_by_browser_global(self, data):
        self.clear_page()
        self.show_graph(data, "Global Browser Stats").pack(side=LEFT, fill=BOTH, expand=True)

    def show_graph(self, data, title):
        figure = Figure(figsize=(5, 5), dpi=100)
        sub_plot = figure.add_subplot(111)
        figure.suptitle(title, fontsize=14)
        width = 0.7
        x_axis_values, y_axis_values, labels = self.__construct_data_for_graph(data)
        sub_plot.bar(x_axis_values, y_axis_values, width)
        sub_plot.set_xticks(x_axis_values + width / 2.0)
        if len(labels) > 5 and len(max(labels, key=lambda l: len(l))) > 2:
            figure.subplots_adjust(bottom=0.3)
            sub_plot.set_xticklabels(labels, rotation=45, ha='right')
        else:
            sub_plot.set_xticklabels(labels)
        sub_plot.autoscale()
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.show()
        self.page_items.append(canvas.get_tk_widget())
        return canvas.get_tk_widget()

    @staticmethod
    def __construct_data_for_graph(data):
        x = np.arange(1, len(data) + 1)
        labels, y = [], []
        for label, val in data.items():
            labels.append(label)
            y.append(val)
        return x, y, labels

    def clear_page(self):
        for item in self.page_items:
            item.pack_forget()


class NavigationPage(Frame):
    def __init__(self, parent, controller, data):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.controller = controller
        self.active_buttons = []
        self.__setup_page(data)
        self.__setup_content(data)

    def __setup_page(self, data):
        label = Label(self, text="Document Tracker Analyser")
        label.grid(column=0, row=0)
        label_header = Label(self, text="Top Readers")
        label_header.grid(column=3, row=0)
        button = Button(self, text="Global browser stats",
                        command=lambda: self.controller.show_graph_page_browser(data.get_views_by_browser_global()))
        button.grid(column=1, row=0)

    def __setup_content(self, data):
        self.__setup_buttons(data)
        self.__setup_readership(data)

    def __setup_readership(self, data):
        readers = sorted(data.visitors.values(), key=lambda r: r.total_view_time, reverse=True)
        for val, reader in enumerate(readers[:10], 1):
            text = str(val) + ": " + reader.uuid[:6] + "..."
            label = Label(self, text=text + " " + str(reader.total_view_time) + " time viewed")
            label.grid(column=3, row=val+2)

    def __find_page(self, doc_id, user_id):
        document = self.controller.data_loader.documents[doc_id]
        user = self.controller.data_loader.documents[user_id] if user_id != '' else None
        self.controller.show_graph_page(document, user=user)

    def __setup_buttons(self, data):

        Label(self, text='Document UUID').grid(column=0, row=1)
        doc_entry = Entry(self)
        doc_entry.grid(column=0, row=2)
        Label(self, text='User UUID (optional)').grid(column=1, row=1)
        user_entry = Entry(self)
        user_entry.grid(column=1, row=2)

        search_button = Button(self, text='Find',
                               command=lambda: self.__find_page(doc_entry.get(), user_entry.get()))
        search_button.grid(column=2, row=2)

        docs = sorted(data.documents.values(), key=lambda document: len(document.views), reverse=True)
        for val, doc in enumerate(docs[:20], 3):
            text = doc.doc_id[:6] + "... "
            button = Button(self, text=text, width=20,
                            command=lambda document=doc: self.controller.show_graph_page(document))
            button.grid(column=0, row=val)
            label = Label(self, text=str(len(doc.views)) + " views")
            label.grid(column=1, row=val)
            self.active_buttons.append((button, label))


class Controller(Tk):
    def __init__(self, file_name, task=None, doc_id=None, only_reads=True, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        Tk.wm_title(self, "Document Tracker Analyser")
        self.style = Style()
        self.data_loader = DataLoader(file_name, only_reads=only_reads)
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.setup_pages(container)

        self.show_frame(NavigationPage)

        if task == '2':
            try:
                self.show_graph_page(self.data_loader.documents[doc_id])
            except KeyError:
                print("Invalid document UUI: "+ doc_id)
                sys.exit(2)
        elif task == '3a':
            self.show_graph_page_browser(self.data_loader.get_views_by_browser_global_base())
        elif task == '3b':
            self.show_graph_page_browser(self.data_loader.get_views_by_browser_global())

    def setup_pages(self, container):
        frame = NavigationPage(container, self, self.data_loader)
        self.frames[NavigationPage] = frame
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
