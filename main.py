import json
from subject import Subject
from visitor import Visitor, DocumentView


class DataLoader:
    def __init__(self, use_test_data=False):
        self.subjects = {}
        self.visitors = {}
        self.load_data(use_test_data)

    def load_data(self, use_test_data):
        json_data = []
        data_file_name = 'json_data/issuu_sample.json' if use_test_data else 'json_data/issuu_cw2.json'
        with open(data_file_name) as f:
            for line in f:
                json_data.append(json.loads(line))

        for view in json_data:
            self.decode_item(view)

    def decode_item(self, item):
        if "subject_doc_id" not in item.keys():
            return
        doc_id = item["subject_doc_id"]
        if doc_id not in self.subjects.keys():
            subject = Subject(doc_id, item["subject_type"])
            self.subjects.update({doc_id: subject})
        else:
            subject = self.subjects[doc_id]
        visitor_id = item["visitor_uuid"]
        if visitor_id not in self.visitors.keys():
            visitor = Visitor(item["visitor_username"] if "visitor_username" in item.keys() else None,
                              visitor_id, item["visitor_source"], item["visitor_useragent"], item["visitor_country"])
            self.visitors.update({visitor_id: visitor})
        else:
            visitor = self.visitors[visitor_id]
        event_readtime = None
        if "event_readtime" in item.keys():
            event_readtime = item["event_readtime"]
        doc_view = DocumentView(visitor, subject, event_readtime, item["subject_page"])
        subject.views.append(doc_view)
        visitor.doc_views.append(doc_view)
