import user_agents
from countryinfo import countries

country_dict = {}

# Reorder countries into a dictionary for faster access
for country_info in countries:
    country_dict.update({country_info["code"]: country_info})


class Reader:
    def __init__(self, username, uuid, source, user_agent, country):
        self.username = username
        self.uuid = uuid
        self.source = source
        # Todo: should country and useragent be in view? do users view from different country and browser?
        self.user_agent = user_agents.parse(user_agent)
        self.country = country
        self.doc_views = []

    def total_view_time(self):
        total_time = 0
        for view in self.doc_views:
            if view.time_viewed is not None:
                total_time += view.time_viewed
        return total_time

    def country_name(self):
        return country_dict[self.country]["name"]

    def continent_name(self):
        return country_dict[self.country]["continent"]


class Document:
    def __init__(self, doc_id, doc_type):
        self.doc_id = doc_id
        self.doc_type = doc_type
        self.views = []

    def get_views_by_country(self):
        return self.get_views_by_key(lambda view: view.visitor.country)

    def get_views_by_continent(self):
        return self.get_views_by_key(lambda view: view.visitor.continent_name())

    def get_views_by_browser(self):
        return self.get_views_by_key(lambda view: view.visitor.user_agent.browser.family)

    def get_views_by_key(self, key):
        views_by_key = {}
        for view in self.views:
            item = key(view)
            if item in views_by_key.keys():
                views_by_key[item] += 1
            else:
                views_by_key.update({item: 1})
        return views_by_key

    def also_likes(self, amount=5):
        readers = [view.visitor for view in self.views]
        doc_views = {}
        for reader in readers:
            for view in reader.doc_views:
                if view.document in doc_views.keys():
                    doc_views[view.document] += 1
                else:
                    doc_views.update({view.document: 1})
        top_docs = sorted(doc_views, key=lambda doc: doc_views[doc], reverse=True)[:amount]
        return top_docs


class DocumentView:
    def __init__(self, visitor, document, time_viewed, page_viewed):
        self.visitor = visitor
        self.document = document
        self.time_viewed = time_viewed
        self.page_viewed = page_viewed
