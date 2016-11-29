import getopt
import sys
from data_loader import DataLoader
from gui_controller import Controller
from gui_controller import sort_by_readtime, sort_by_views


def start_gui(task=None, doc_id=None):
    app = Controller(task=task, doc_id=doc_id)
    app.mainloop()
    return app


def main():
    argv = (sys.argv[1:])
    doc_id, task_id, user_id = get_args(argv)
    run_task(doc_id, task_id, user_id)


def get_args(argv):
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
    return doc_id, task_id, user_id


def run_task(doc_id, task_id, user_id):
    if task_id == '2a' or task_id == '2b' or task_id == '2':
        requires_error(doc_id is None, "No document id given")
        start_gui(task='2', doc_id=doc_id)
    elif task_id == '3a':
        start_gui(task=task_id)
    elif task_id == '3b':
        start_gui(task=task_id)
    elif task_id == '4':
        task_4()
    elif task_id == '5a':
        task_5(sort_by_views, doc_id, user_id)
    elif task_id == '5b':
        task_5(sort_by_readtime, doc_id, user_id)
    else:
        start_gui()


def task_4():
    data = DataLoader(only_reads=False)
    readers = sorted(data.visitors.values(), key=lambda r: r.total_view_time(), reverse=True)
    for val, reader in enumerate(readers[:10], 1):
        print(str(val) + ": " + reader.uuid)


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
    main()
