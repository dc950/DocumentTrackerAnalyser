import json
from view_data import Reader, Document, DocumentView


class DataLoader:
    def __init__(self, use_test_data=False, only_reads=False):
        self.documents = {}
        self.visitors = {}
        self.__load_data(use_test_data, only_reads)

    def __load_data(self, use_test_data, only_reads):
        json_data = []
        data_file_name = 'json_data/issuu_sample.json' if use_test_data else 'json_data/issuu_cw2.json' #'json_data/sample_100k_lines.json'
        with open(data_file_name) as f:
            for line in f:
                json_data.append(json.loads(line))

        for view in json_data:
            self.__decode_item(view, only_reads)

    def __decode_item(self, item, only_reads):
        if "subject_doc_id" not in item:
            return
        if only_reads and item["event_type"] != "read" and item["event_type"] != "pagereadtime":
            return
        document = self.__create_document(item)
        reader = self.__create_reader(item)
        event_readtime = item.get("event_readtime")
        doc_view = DocumentView(reader, document, event_readtime,  item["visitor_useragent"], item["visitor_country"])
        document.views.append(doc_view)
        reader.doc_views.append(doc_view)

    def __create_reader(self, item):
        visitor_id = item["visitor_uuid"]
        if visitor_id not in self.visitors:
            reader = Reader(item["visitor_username"] if "visitor_username" in item else None,
                            visitor_id, item["visitor_source"])
            self.visitors.update({visitor_id: reader})
        else:
            reader = self.visitors[visitor_id]
        return reader

    def __create_document(self, item):
        doc_id = item["subject_doc_id"]
        if doc_id not in self.documents:
            document = Document(doc_id, item["subject_type"])
            self.documents.update({doc_id: document})
        else:
            document = self.documents[doc_id]
        return document

    def get_views_by_browser_global_base(self):
        return self.get_global_view_data(lambda view: view.user_agent_string)

    def get_views_by_browser_global(self):
        return self.get_global_view_data(lambda view: view.user_agent)

    def get_global_view_data(self, key):
        global_data = {}
        views = (view for visitor in self.visitors.values() for view in visitor.doc_views)
        for view in views:
            item = key(view)
            if item in global_data:
                global_data[item] += 1
            else:
                global_data.update({item: 1})
        return global_data
