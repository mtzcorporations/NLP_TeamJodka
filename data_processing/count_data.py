import json

v1_path = "../data/translations/test_slo.json"
v2_path = "../data/translations/test_v2_slo.json"

with open(v1_path, encoding='utf-8') as f:
    v1_set = json.load(f)

with open(v2_path, encoding='utf-8') as f:
    v2_set = json.load(f)

total_answers = 0
total_questions_pos = 0
total_questions_imposs = 0
total_contexts = 0
checked = []

for question in v2_set["data"]:
    if len(question["answers"]["text"]) == 0:
        total_questions_imposs += 1
        continue
    id_q = question["id"].split("_")
    index_doc = int(id_q[0])
    index_paragraph = int(id_q[1])
    if (index_doc, index_paragraph) not in checked:
        checked.append((index_doc, index_paragraph))
        total_contexts += 1
    total_questions_pos += 1
    total_answers += len(question["answers"]["text"])

print("Total Questions:", total_questions_pos + total_questions_imposs, len(v2_set["data"]))
print("Total Answerable Questions:", total_questions_pos)
print("Total Impossible Questions:", total_questions_imposs)
print("Total Answers:", total_answers)
print("Total Contexts:", total_contexts)