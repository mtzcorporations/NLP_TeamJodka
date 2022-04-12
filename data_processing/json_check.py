import json

file1 = "../data/dev-v2.0.json"
file2 = "output/dev-v2.0_translated.json"

with open(file1, encoding="utf8") as f:
    dataset = json.load(f)
with open(file2, encoding="utf8") as f:
    dataset_english = json.load(f)

if len(dataset["data"]) != len(dataset_english["data"]):
    print("Data # Error")
for d_i, document in enumerate(dataset["data"]):
    en_ver = dataset_english["data"][d_i]
    if len(document["paragraphs"]) != len(en_ver["paragraphs"]):
        print("Paragraph # Error", d_i)
    for p_i, paragraph in enumerate(document["paragraphs"]):
        en_ver = dataset_english["data"][d_i]["paragraphs"][p_i]
        if len(paragraph["qas"]) != len(en_ver["qas"]):
            print("QAS # Error", d_i, p_i)
        for q_i, qas in enumerate(paragraph["qas"]):
            en_ver = dataset_english["data"][d_i]["paragraphs"][p_i]["qas"][q_i]
            if len(qas["answers"]) != len(en_ver["answers"]):
                print("QAS # Error", d_i, p_i, q_i)