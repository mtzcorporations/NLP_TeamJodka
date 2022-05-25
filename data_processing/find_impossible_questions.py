# importing pandas as pd
import os
import pandas as pd
import json
import csv

def csv_to_excel(input_file, output_file):
    read_file = pd.read_csv(input_file)

    read_file.to_excel(output_file, index=None, header=False)

def find_impossible_questions(data_path_eng, data_path_slo, data_path_translated_slo, output_name):
    with open(data_path_eng, encoding='utf-8') as f:
        data_eng = json.load(f)["data"]

    with open(data_path_slo, encoding='utf-8') as f:
        data_slo = json.load(f)["data"]

    with open(data_path_translated_slo, encoding='utf-8') as f:
        data_translated_slo = json.load(f)

    impossible_questions = []
    checked = []
    for question in data_translated_slo["data"]:
        id_q = question["id"].split("_")
        index_doc = int(id_q[0])
        index_paragraph = int(id_q[1])
        if (index_doc, index_paragraph) in checked:
            continue
        checked.append((index_doc, index_paragraph))
        qas_eng = data_eng[index_doc]["paragraphs"][index_paragraph]
        qas_slo = data_slo[index_doc]["paragraphs"][index_paragraph]
        context_eng = qas_eng["context"]
        context_slo = question["context"]
        for i, question_original in enumerate(qas_eng["qas"]):
            if question_original["is_impossible"]:
                question_slo = qas_slo["qas"][i]["question"]
                impossible_questions.append((f'{index_doc}_{index_paragraph}_{i}' ,
                                             context_eng, question_original["question"],
                                             context_slo, question_slo))


    with open("output/temp.csv", 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["eng", "slo"])
        for impossible_question in impossible_questions:
            writer.writerow([impossible_question[0], impossible_question[0]])
            writer.writerow([impossible_question[1], impossible_question[3]])
            writer.writerow([impossible_question[2], impossible_question[4]])

    csv_to_excel("output/temp.csv", os.path.join("output", output_name + ".xlsx"))
    os.remove("output/temp.csv")

if __name__ == '__main__':
    find_impossible_questions("../data/dev-v2.0.json", "./output/dev-v2.0_translated_corrected.json",
                          "../data/translations/test_slo.json", "impossible_questions")
