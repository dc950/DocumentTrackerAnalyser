import user_agents


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


class Document:
    def __init__(self, doc_id, doc_type):
        self.doc_id = doc_id
        self.doc_type = doc_type
        self.views = []

    def get_views_by_country(self):
        return self.get_views_by_key(lambda view: view.visitor.country)

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


class DocumentView:
    def __init__(self, visitor, document, time_viewed, page_viewed):
        self.visitor = visitor
        self.document = document
        self.time_viewed = time_viewed
        self.page_viewed = page_viewed


