# importing pandas as pd
import random

import pandas as pd
import json
import csv
import numpy as np


def csv_to_excel(input_file, output_file):
    read_file = pd.read_csv(input_file)

    read_file.to_excel(output_file, index=None, header=False)

def excel_to_csv(input_file, output_file):
    # Read and store content
    # of an excel file
    read_file = pd.read_excel(input_file)

    # Write the dataframe object
    # into csv file
    read_file.to_csv(output_file,
                     index=None,
                     header=False)

    # read csv file and convert
    # into a dataframe object
    df = pd.DataFrame(pd.read_csv(output_file))

    # show the dataframe
    print(df)

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

            writer.writerow([id_eng, id_slo])
            writer.writerow([context_eng, context_slo])

            for j in range(len(excel_data_eng_n[i][1]["qas"])):
                if excel_data_eng_n[i][1]["qas"][j]["is_impossible"]:
                    continue
                question_eng = excel_data_eng_n[i][1]["qas"][j]["question"]
                question_slo = excel_data_slo_n[i][1]["qas"][j]["question"]
                writer.writerow([question_eng, question_slo])
                for k in range(len(excel_data_eng_n[i][1]["qas"][j]["answers"])):
                    answer_eng = excel_data_eng_n[i][1]["qas"][j]["answers"][k]["text"]
                    answer_slo = excel_data_slo_n[i][1]["qas"][j]["answers"][k]["text"]
                    writer.writerow([answer_eng, answer_slo])

    csv_to_excel("out.csv", "excel_za_meto.xlsx")

create_random_data("../data/train-v2.0.json", "./output/train-v2.0_translated.json", "out.csv", 3)


#excel_to_csv("Test.xlsx", "Test.csv")

