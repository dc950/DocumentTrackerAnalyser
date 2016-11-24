

class Subject:
    def __init__(self, doc_id, doc_type):
        self.doc_id = doc_id
        self.doc_type = doc_type
        self.views = []

    def get_views_by_country(self):
        views_by_country = {}
        print(len(self.views))
        for item in self.views:
            country = item.visitor.country
            if country in views_by_country.keys():
                views_by_country[country] += 1
            else:
                views_by_country.update({country: 1})
        return views_by_country
