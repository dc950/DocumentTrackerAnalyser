import json
from view_data import Reader, Document, DocumentView


class DataLoader:
    def __init__(self, use_test_data=False):
        self.documents = {}
        self.visitors = {}
        self.__load_data(use_test_data)

    def __load_data(self, use_test_data):
        json_data = []
        data_file_name = 'json_data/issuu_sample.json' if use_test_data else 'json_data/issuu_cw2.json' #'json_data/sample_100k_lines.json'
        with open(data_file_name) as f:
            for line in f:
                json_data.append(json.loads(line))

        for view in json_data:
            self.decode_item(view)

    def decode_item(self, item):
        if "subject_doc_id" not in item:
            return
        if item["event_type"] != "read" and item["event_type"] != "pagereadtime":
            return
        doc_id = item["subject_doc_id"]
        if doc_id not in self.documents:
            document = Document(doc_id, item["subject_type"])
            self.documents.update({doc_id: document})
        else:
            document = self.documents[doc_id]
        visitor_id = item["visitor_uuid"]
        if visitor_id not in self.visitors:
            reader = Reader(item["visitor_username"] if "visitor_username" in item else None,
                            visitor_id, item["visitor_source"], item["visitor_useragent"], item["visitor_country"])
            self.visitors.update({visitor_id: reader})
        else:
            reader = self.visitors[visitor_id]
        event_readtime = None
        if "event_readtime" in item:
            event_readtime = item["event_readtime"]
        doc_view = DocumentView(reader, document, event_readtime, item["subject_page"])
        document.views.append(doc_view)
        reader.doc_views.append(doc_view)

    def get_views_by_browser_global_base(self):
        return self.get_visitor_global_data(lambda x: x.user_agent_string)

    def get_views_by_browser_global(self):
        return self.get_visitor_global_data(lambda x: x.user_agent)

    def get_visitor_global_data(self, key):
        global_data = {}
        for visitor in self.visitors.values():
            item = key(visitor)
            if item in global_data:
                global_data[item] += 1
            else:
                global_data.update({item: 1})
        return global_data
