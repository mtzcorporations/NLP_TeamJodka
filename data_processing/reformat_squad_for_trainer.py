import json
import argparse


def reformat_data(data_path, output_path):
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
    with open(output_path, "w", encoding="utf8") as f:
        f.write(json.dumps(json_new, ensure_ascii=False))
    return trainer_data


if __name__ == '__main__':
    # reformat_data('../data/dev-v2.0.json',
    #               "../data_processing/output/rf_dev-v2.0_ENG.json")
    # reformat_data( '../data/train-v2.0.json',
    #               "../data_processing/output/rf_train-v2.0_ENG.json")
    # reformat_data('../data_processing/output/dev-v2.0_normalized.json',
    #               "../data_processing/output/rf_dev-v2.0_ENG_normalized.json")
    # reformat_data( '../data_processing/output/train-v2.0_normalized.json',
    #               "../data_processing/output/rf_train-v2.0_ENG_normalized.json")
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file", required=True)
    parser.add_argument("-o", "--output", help="Output file.", required=True)
    args = parser.parse_args()
    print(args)
    reformat_data(args.input, args.output)
