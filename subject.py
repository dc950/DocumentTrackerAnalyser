from pprint import pprint

class Subject:
    def __init__(self, doc_id, doc_type):
        self.doc_id = doc_id
        self.doc_type = doc_type
        self.views = []

    def print_views_by_country(self):
        views_by_country = {}
        for item in self.views:
            country = item['visitor_country']
            if country in views_by_country.keys():
                views_by_country[country] += 1
            else:
                views_by_country.update({country: 1})
        print("Document: " + self.doc_id + "\nTotal views: " + str(len(self.views)))
        pprint(views_by_country)

    def add_view(self, new_view):
        self.views.append(new_view)
