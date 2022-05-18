from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer
import json

def fix_csv(csv_path, number):
    with open(csv_path, 'r', encoding='utf-8') as f:
        fix = open('../data_processing/output/fixed_csv' + number + '.txt', 'w', encoding='utf-8')
        while True:
            line = f.readline()
            if line == '"\n':
                continue
            line = line.replace('"', '')
            if line == "":
                break
            # print(line)
            # data = line.rstrip('\n').rstrip('\r').split(";")
            fix.write(line)
        fix.close()


def create_json_from_translations(paths, tip):
    # data_dict = {"data": []}
    reformated_data = []
    for path in paths:
        with open(path, 'r', encoding='utf-8-sig') as f:
            while True:
                line = f.readline()
                if line == "":
                    break
                data = line.rstrip('\n').rstrip('\r').split(";")
                # qas = []
                # print(data)
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
    with open("../data_processing/output/prevod_" + tip + ".json", "w", encoding="utf8") as f:
        f.write(json.dumps(json_new, ensure_ascii=False))

    # with open("../data_processing/output/prevod_meta.json", "w", encoding="utf8") as f:
    #     f.write(json.dumps(data_dict, ensure_ascii=False))


def evaluate_json(data_path, model_name_or_path, cache_dir):
    tokenizer = AutoTokenizer.from_pretrained(
        model_name_or_path,
        cache_dir=cache_dir,
        use_fast=True,
        revision="main",
        use_auth_token=None,
    )
    model = AutoModelForQuestionAnswering.from_pretrained(
        model_name_or_path,
        from_tf=bool(".ckpt" in model_name_or_path),
        # config=config,
        cache_dir=cache_dir,
        revision="main",
        use_auth_token=None,
    )
    nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    all_questions = 0
    correct_answers = 0
    for item in data["data"]:
        all_questions += 1
        context = item["context"]
        question = item["question"]
        answers = item["answers"]
        QA_input = {
            'question': question,
            'context': context
        }
        res = nlp(QA_input)
        # print("Result: ", res)
        # print("True answers: ", answers)
        res = res["answer"]
        result = res.strip()
        if result[-1] in [".", "!", "?", ",", ":"]:
            result = result[:-1]
        found_answer = False
        for answer in answers:
            if result == answer["text"]:
                correct_answers += 1
                found_answer = True
                break
        if not found_answer:
            print(res)
            print(answers)

    print("All questions: ", all_questions)
    print("Correct answers: ", correct_answers)
    print("Final score: ", correct_answers / all_questions)


# fix_csv("Drugi_prevodi_final.csv", "2")
create_json_from_translations(["../data_processing/output/fixed_csv2.txt", "../data_processing/output/fixed_csv3.txt", "../data_processing/output/fixed_csv4.txt"], "meta")
# create_json_from_translations(["./drugi_prevodi_auto.csv", "./tretji_prevodi_auto.csv", "./cetrti_prevodi_auto.csv"], "auto")


# evaluate_json("../data_processing/output/prevod_meta.json", "deepset/xlm-roberta-large-squad2", "../cache")
