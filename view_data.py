import itertools
from ua_parser import user_agent_parser
from countryinfo import country_to_continent, continents

#  This prevents views having to re-parse their user_agent_strings if an identical one has already been parsed
parsed_user_agents = {}


class Reader:
    def __init__(self, uuid, ):
        self.uuid = uuid
        self.doc_views = []

    def __repr__(self):
        return "<Reader " + self.uuid + ">"

    def __str__(self):
        return self.uuid

    @property
    def total_view_time(self):
        total_time = 0
        for view in self.doc_views:
                total_time += view.time_viewed or 0
        return total_time


class Document:
    def __init__(self, doc_id, doc_type):
        self.doc_id = doc_id
        self.doc_type = doc_type
        self.views = []

    def __repr__(self):
        return "<Document " + self.doc_id + ">"

    def __str__(self):
        return self.doc_id

    @property
    def views_by_country(self):
        return self.get_views_by_key(lambda view: view.country)

    @property
    def views_by_continent(self):
        return self.get_views_by_key(lambda view: view.continent_name)

    @property
    def views_by_browser(self):
        return self.get_views_by_key(lambda view: view.user_agent)

    def get_views_by_key(self, key_function):
        """
        Returns a dictionary of view to number to determine the number of views over a certain property
        within each view
        :param key_function: a function to obtain the the field by which to categorise the views
        :return: A dictionary of some type to int where the int is the number of views for a certain property
        (defined in the function key) is the value of the dict key
        """
        views_by_key = {}
        self.also_likes()
        for view in self.views:
            item = key_function(view)
            if item in views_by_key:
                views_by_key[item] += 1
            else:
                views_by_key.update({item: 1})
        return views_by_key

    def also_likes(self, sort=None, amount=10, user=None):
        """
        Finds documents also read by users whom have read this
        :param sort: A function to sort the documents
        :param amount: The number of documents to be returned
        :param user: The user who is viewing the document (will be ignored)
        :return: a list of tuples which each contain: (document, [views, view time])
        """
        doc_views = {}
        # define generator of readers, not including input one
        readers = (view.visitor for view in self.views if view.visitor is not user)
        readers = self.__remove_duplicates(readers)

        for reader in readers:
            already_read = set()  # used to prevent counting multiple views of the same document for one user
            for view in reader.doc_views:
                document = view.document
                if document is self:
                    continue
                if document in doc_views:
                    if document not in already_read:
                        doc_views[document][0] += 1
                        already_read.add(document)
                    doc_views[document][1] += view.time_viewed or 0  # If the time is None, nothing is added
                else:
                    doc_views.update({document: [1, view.time_viewed or 0]})
                    already_read.add(document)
        if sort is not None:
            top_docs = list(sort(doc_views))[:amount]
        else:
            chosen_docs = itertools.islice(doc_views.keys(), 0, amount)
            top_docs = []
            for doc in chosen_docs:
                top_docs.append((doc, doc_views[doc]))
        return top_docs

    @staticmethod
    def __remove_duplicates(values):
        seen = set()
        for value in values:
            if value not in seen:
                seen.add(value)
                yield value


class DocumentView:
    def __init__(self, visitor, document, time_viewed, user_agent_string, country):
        self.visitor = visitor
        self.document = document
        self.time_viewed = time_viewed
        self.user_agent_string = user_agent_string
        #  self.__user_agent = None
        self.country = country

    def __repr__(self):
        return '<DocumentView between ' + self.document + ' & ' + self.visitor + '>'

    def __str__(self):
        return 'Document view between document ' + str(self.document) + ' & visitor ' + str(self.visitor) + '>'

    @property
    def user_agent(self):
        if self.user_agent_string not in parsed_user_agents:
            parsed_user_agents[self.user_agent_string] = \
                user_agent_parser.ParseUserAgent(self.user_agent_string)["family"]
        return parsed_user_agents[self.user_agent_string]

    @property
    def continent_name(self):
        return continents[country_to_continent[self.country]]
