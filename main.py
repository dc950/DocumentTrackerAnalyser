import json
from subject import Subject
from visitor import Visitor, DocumentView
from incf.countryutils import transformations

json_data = []
with open('json_data/issuu_sample.json') as f:
    for line in f:
        json_data.append(json.loads(line))

subjects = {}
visitors = {}


def decode_item(item):
    if "subject_doc_id" not in item.keys():
        return
    doc_id = item["subject_doc_id"]
    if doc_id not in subjects.keys():
        subject = Subject(doc_id, item["subject_type"])
        subjects.update({doc_id: subject})
    else:
        subject = subjects[doc_id]
    visitor_id = item["visitor_uuid"]
    if visitor_id not in visitors.keys():
        visitor = Visitor(item["visitor_username"], visitor_id, item["visitor_source"], item["visitor_useragent"],
                          item["visitor_country"])
        visitors.update({visitor_id: visitor})
    else:
        visitor = visitors[visitor_id]
    event_readtime = None
    if "event_readtime" in item.keys():
        event_readtime = item["event_readtime"]
    doc_view = DocumentView(visitor, subject, event_readtime, item["subject_page"])
    subject.views.append(doc_view)
    visitor.doc_views.append(doc_view)


for view in json_data:
    decode_item(view)

print("Total number of subjects: " + str(len(subjects)))
print("Total number of views: " + str(len(json_data)))

for doc in subjects.values():
    country_data = doc.print_views_by_country()
    print(doc.doc_id)
    for country, count in country_data.items():
        print(transformations.cc_to_cn(country) + ":", count)
