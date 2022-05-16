from transformers import pipeline
import json


def read_translated_csv(path):
    # data_dict = {"data": []}
    reformated_data = []
    with open(path, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            # if line == '"\n':
            #     continue
            line = line.replace('"', '')
            if line == "":
                break

            data = line.rstrip('\n').rstrip('\r').split(";")
            # qas = []
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
                    # qas.append({"question": question, "answers": answers})

                    reformated_data.append({"id": data[0], "title": "", "context": context, "question": question, "answers": answers})

                # data_dict["data"].append({"id": data[0], "qas": qas, "context": context})

    json_new = {"version": "v2.0", "data": reformated_data}
    with open("../data_processing/output/prevod_meta.json", "w", encoding="utf8") as f:
        f.write(json.dumps(json_new, ensure_ascii=False))

    # with open("../data_processing/output/prevod_meta.json", "w", encoding="utf8") as f:
    #     f.write(json.dumps(data_dict, ensure_ascii=False))

def get_prediction(model_name, question, context):
    nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
    QA_input = {
        'question': question,
        'context': context
    }
    res = nlp(QA_input)
    print(res)
    return res

def evaluate(data_path, model_name):
    read_translated_csv(data_path)
    # get_prediction(model_name, "Who like's stones?", "Davor likes stones.")

evaluate("./Drugi_prevodi_final.csv", "deepset/xlm-roberta-large-squad2")