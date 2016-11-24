import user_agents


class Visitor:
    def __init__(self, username, uuid, source, user_agent_string, country):
        self.username = username
        self.uuid = uuid
        self.source = source
        self.country = country
        self.user_agent = user_agents.parse(user_agent_string)
        self.doc_views = []


class DocumentView:
    def __init__(self, visitor, document, time_viewed, page_viewed):
        self.visitor = visitor
        self.document = document
        self.time_viewed = time_viewed
        self.page_viewed = page_viewed
