import json


def reformat_data(data_path, outputh_path):
    with open(data_path, 'r', encoding='utf-8') as f:
        data_eng = json.load(f)

    trainer_data = []
    for item in data_eng["data"]:
        for paragraph in item["paragraphs"]:
            for qa in paragraph["qas"]:
                answers = {"text": [], "answer_start": []}
                pog = False
                for answer in qa["answers"]:
                    if(int(answer["answer_start"])!=-1):
                        pog=True
                        answers["text"].append(answer["text"])
                        answers["answer_start"].append(answer["answer_start"])
                if(pog):
                    trainer_data.append({"id": qa["id"], "title": item["title"], "context": paragraph["context"], "question": qa["question"], "answers": answers})
                elif(qa["is_impossible"]):
                    trainer_data.append({"id": qa["id"], "title": item["title"], "context": paragraph["context"],
                                         "question": qa["question"], "answers": answers})

    json_new = {"version": "v2.0", "data": trainer_data}
    with open(outputh_path, "w", encoding="utf8") as f:
        f.write(json.dumps(json_new, ensure_ascii=False))
    return trainer_data


reformat_data('../data_processing/output/dev-v2.0_translated_corrected.json',"../data_processing/output/rf_dev-v2.0_SLO_translated_corrected.json")
reformat_data( '../data_processing/output//train-v2.0_translated_corrected.json',"../data_processing/output/rf_train-v2.0_SLO_translated_corrected.json")