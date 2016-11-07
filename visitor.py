class Visitor:
    def __init__(self, username, uuid, source, user_agent_string, country):
        self.username = username
        self.uuid = uuid
        self.source = source
        self.country = country
        self.user_agent = self.get_user_agent(user_agent_string.lower())
        self.doc_views = []

    @staticmethod
    def get_user_agent(user_agent_string):
        # TODO: update with an enumerator or something
        user_agent_string = user_agent_string.lower()
        if "mozilla" in user_agent_string:
            return "Mozilla Firefox"
        elif "internet explorer" in user_agent_string:
            return "Internet Explorer"
        elif "chrome" in user_agent_string:
            return "Google Chrome"
        elif "safari" in user_agent_string:
            return "Safari"


class DocumentView:
    def __init__(self, visitor, document, time_viewed, page_viewed):
        self.visitor = visitor
        self.document = document
        self.time_viewed = time_viewed
        self.page_viewed = page_viewed
