import user_agents


class Reader:
    def __init__(self, username, uuid, source, user_agent_string, country):
        self.username = username
        self.uuid = uuid
        self.source = source
        self.country = country
        self.user_agent = user_agents.parse(user_agent_string)
        self.doc_views = []


class Document:
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


class DocumentView:
    def __init__(self, visitor, document, time_viewed, page_viewed):
        self.visitor = visitor
        self.document = document
        self.time_viewed = time_viewed
        self.page_viewed = page_viewed
