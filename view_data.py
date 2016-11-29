from ua_parser import user_agent_parser
from countryinfo import country_to_cont, continents


class Reader:
    def __init__(self, username, uuid, source, user_agent, country):
        self.username = username
        self.uuid = uuid
        self.source = source
        # Todo: should country and useragent be in view? do users view from different countries and browsers?
        self.user_agent_string = user_agent
        self.__user_agent_cache = None
        self.country = country
        self.doc_views = []

    @property
    def user_agent(self):
        if self.__user_agent_cache is None:
            self.__user_agent_cache = user_agent_parser.ParseUserAgent(self.user_agent_string)["family"]
        return self.__user_agent_cache

    def total_view_time(self):
        total_time = 0
        for view in self.doc_views:
            if view.time_viewed is not None:
                total_time += view.time_viewed
        return total_time

    def continent_name(self):
        return continents[country_to_cont[self.country]]


class Document:
    def __init__(self, doc_id, doc_type):
        self.doc_id = doc_id
        self.doc_type = doc_type
        self.views = []

    def __repr__(self):
        return "<Document " + self.doc_id + ">"

    def get_views_by_country(self):
        return self.get_views_by_key(lambda view: view.visitor.country)

    def get_views_by_continent(self):
        return self.get_views_by_key(lambda view: view.visitor.continent_name())

    def get_views_by_browser(self):
        return self.get_views_by_key(lambda view: view.visitor.user_agent)

    def get_views_by_key(self, key):
        views_by_key = {}
        for view in self.views:
            item = key(view)
            if item in views_by_key:
                views_by_key[item] += 1
            else:
                views_by_key.update({item: 1})
        return views_by_key

    def also_likes(self, sort, amount=10, user=None):
        readers = (view.visitor for view in self.views if view.visitor != user)
        doc_views = {}
        for reader in readers:
            for view in reader.doc_views:
                document = view.document
                if document is self:
                    continue
                if document in doc_views:
                    doc_views[document][0] += 1
                    doc_views[document][1] += view.time_viewed or 0
                else:
                    doc_views.update({document: [1, view.time_viewed or 0]})
        top_docs = sort(doc_views)[:amount]
        return top_docs


class DocumentView:
    def __init__(self, visitor, document, time_viewed, page_viewed):
        self.visitor = visitor
        self.document = document
        self.time_viewed = time_viewed
        self.page_viewed = page_viewed
