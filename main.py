import json
from subject import Subject
from visitor import Visitor

data = []
with open('data/issuu_cw2.json') as f:
    for line in f:
        data.append(json.loads(line))

subjects = {}


def decode_item(item):
    if "subject_doc_id" not in item.keys():
        return
    doc_id = item["subject_doc_id"]
    if doc_id not in subjects.keys():
        subject = Subject(doc_id, item["subject_type"])
        subjects.update({doc_id: subject})
    else:
        subject = subjects[doc_id]
    subject.add_view(item)

for view in data:
    decode_item(view)

print("Total number of subjects: "+str(len(subjects)))
print("Total number of views: "+str(len(data)))
counter = 20
for doc in subjects.values():
    doc.print_views_by_country()








