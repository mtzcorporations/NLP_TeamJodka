# importing pandas as pd
import random

import pandas as pd
import json
import csv
import numpy as np


def csv_to_excel(input_file, output_file):
    read_file = pd.read_csv(input_file)

    read_file.to_excel(output_file, index=None, header=False)


def read_translated_csv(path):
    data_dict = {"data": []}
    with open(path, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if line == "":
                break
            data = line.rstrip('\n').rstrip('\r').split(";")
            qas = []
            if "_" in line and "#" in line and data[0] == data[1]:
                podatki = data[0].split("#")
                num_of_questions = int(len(podatki) / 2)
                num_of_answers = []
                for i, item in enumerate(podatki):
                    if i % 2 != 0:
                        item = item.split("-")
                        num_of_answers.append(len(item))

                context = f.readline().rstrip('\n').rstrip('\r').split(";")[1]
                for i in range(num_of_questions):
                    answers = []
                    question = f.readline().rstrip('\n').rstrip('\r').split(";")[1]
                    for j in range(num_of_answers[i]):
                        answers.append({"text": f.readline().rstrip('\n').rstrip('\r').split(";")[1]})
                    qas.append({"question": question, "answers": answers})

                data_dict["data"].append({"id": data[0], "qas": qas, "context": context})

    with open("./output/prevod_meta.json", "w", encoding="utf8") as f:
        f.write(json.dumps(data_dict, ensure_ascii=False))


def create_random_data(data_path_eng, data_path_slo, output_path, n_samples):
    f = open(data_path_eng, encoding='utf-8')
    data_eng = json.load(f)

    # data_len = len(data_eng['data'])
    excel_data_eng = []
    for i, item in enumerate(data_eng['data']):
        # paragraph_len = len(item['paragraphs'])
        # random_paragraphs = random.sample(item['paragraphs'], 5)
        # excel_data_eng += item['paragraphs']
        for j, paragraph in enumerate(item['paragraphs']):
            id_p = str(i) + "_" + str(j)
            excel_data_eng.append((id_p, paragraph))
    f.close()

    f = open(data_path_slo, encoding='utf-8')
    data_slo = json.load(f)
    excel_data_slo = []
    for i, item in enumerate(data_slo['data']):
        # paragraph_len = len(item['paragraphs'])
        # random_paragraphs = random.sample(item['paragraphs'], 5)
        # excel_data_slo += item['paragraphs']
        for j, paragraph in enumerate(item['paragraphs']):
            id_p = str(i) + "_" + str(j)
            excel_data_slo.append((id_p, paragraph))
    f.close()

    idx = np.random.choice(np.arange(len(excel_data_eng)), n_samples, replace=False)
    excel_data_eng_n = []
    excel_data_slo_n = []
    for i in idx:
        excel_data_eng_n.append(excel_data_eng[i])
        excel_data_slo_n.append(excel_data_slo[i])

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["eng", "slo"])
        for i in range(len(excel_data_eng_n)):
            id_eng = excel_data_eng_n[i][0]
            id_slo = excel_data_slo_n[i][0]
            context_eng = excel_data_eng_n[i][1]["context"]
            context_slo = excel_data_slo_n[i][1]["context"]

            answerable_questions = 0
            qa_ids = ""
            data_under_context = []  # tukaj notri so vprasanja in odgovori
            for j in range(len(excel_data_eng_n[i][1]["qas"])):
                if excel_data_eng_n[i][1]["qas"][j]["is_impossible"]:
                    continue
                question_eng = excel_data_eng_n[i][1]["qas"][j]["question"]
                question_slo = excel_data_slo_n[i][1]["qas"][j]["question"]
                answer_counter = 0
                for k in range(len(excel_data_eng_n[i][1]["qas"][j]["answers"])):
                    if excel_data_slo_n[i][1]["qas"][j]["answers"][k]["answer_start"] == -1:
                        continue
                    answer_counter += 1
                    if answer_counter == 1:
                        answerable_questions += 1
                        data_under_context.append([question_eng, question_slo])
                        qa_ids += str(j) + "#"
                    #   writer.writerow([question_eng, question_slo])  # uprasanje zapisemo ce ima usaj en odgovor
                    answer_eng = excel_data_eng_n[i][1]["qas"][j]["answers"][k]["text"]
                    answer_slo = excel_data_slo_n[i][1]["qas"][j]["answers"][k]["text"]
                    qa_ids += str(k) + "-"
                    data_under_context.append([answer_eng, answer_slo])
                # writer.writerow([answer_eng, answer_slo])
                if qa_ids.endswith("-"):
                    qa_ids = qa_ids[:-1] + "#"
            if answerable_questions > 0:
                writer.writerow([id_eng + "_" + qa_ids, id_slo + "_" + qa_ids])
                writer.writerow([context_eng, context_slo])
                writer.writerows(data_under_context)

    csv_to_excel(output_path, "./output/excel_za_meto.xlsx")


# create_random_data("../data/dev-v2.0.json", "./output/dev-v2.0_translated_corrected.json", "./output/out.csv", 10)
# read_translated_csv("./output/excel_za_meto.csv")
# read_translated_csv("./input/prvi_prevodi_Meta_popravljeno.csv")

# excel_to_csv("Test.xlsx", "Test.csv")
