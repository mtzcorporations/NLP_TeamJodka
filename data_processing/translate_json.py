import glob
import json
import copy
import os
import re
import classla
from pathlib import Path


def json_to_html(input_english_json, input_translated_html, output_path):
    # classla.download('sl')
    # nlp = classla.Pipeline('sl', processors='tokenize,ner,pos,lemma,depparse')

    with open(input_english_json, encoding="utf8") as f:
        json_english = json.load(f)

    json_output = copy.deepcopy(json_english)

    if not isinstance(input_translated_html, list):
        input_translated_html = [input_translated_html]

    indexes = {}
    for input_html in input_translated_html:
        f = open(input_html, encoding="utf8")
        for line in f.readlines():
            if re.match(r"<[^/]*_\d+>", line):
                line = line.replace("<", "").replace(">", "")
                line = line.rsplit("_", 1)
                if line[0] == "answers":
                    has_answer = True
                elif line[0] == "plausible_answers":
                    has_answer = False
                indexes[line[0]] = int(line[1])
                continue
            if "<question>" in line:
                line = line.replace("<question>", "").replace("</question>", "").replace("\n", "")
                json_output["data"][indexes["data"]]["paragraphs"][indexes["paragraphs"]]["qas"][indexes["qas"]][
                    "question"] = line
                continue
            if "<text>" in line:
                line = line.replace("<text>", "").replace("</text>", "").replace("\n", "")
                # a = doc = nlp(line)
                if has_answer:
                    answer_type = "answers"
                else:
                    answer_type = "plausible_answers"

                json_output["data"][indexes["data"]]["paragraphs"][indexes["paragraphs"]]["qas"][indexes["qas"]][
                    answer_type][indexes[answer_type]]["text"] = line
                continue
            if "<context>" in line:
                line = line.replace("<context>", "").replace("</context>", "").replace("\n", "")
                json_output["data"][indexes["data"]]["paragraphs"][indexes["paragraphs"]]["context"] = line
        f.close()

    log = open("log.txt", "w", encoding="utf8")
    total = 0
    found = 0
    for d_i, document in enumerate(json_output["data"]):
        for p_i, paragraph in enumerate(document["paragraphs"]):
            for q_i, qas in enumerate(paragraph["qas"]):
                for a_i, answer in enumerate(qas["answers"]):
                    total += 1
                    index = paragraph["context"].find(answer["text"])
                    json_output["data"][d_i]["paragraphs"][p_i]["qas"][q_i]["answers"][a_i]["answer_start"] = index
                    if index != -1:
                        found += 1
                    else:
                        log.write(json_english["data"][d_i]["paragraphs"][p_i]["qas"][q_i]["answers"][a_i]["text"] +
                                  " | " + answer["text"] + "\n")
    log.close()
    print(f"Found fraction: {(found / total):.2f}")
    output_file_name = Path(input_english_json).stem
    with open(os.path.join(output_path, output_file_name + "_translated.json"), "w", encoding="utf8") as f:
        f.write(json.dumps(json_output, ensure_ascii=False))


if __name__ == '__main__':
    json_to_html("../data/dev-v2.0.json", "input/output_SL.html", "output")
    # json_to_html("../data/train-v2.0.json", ["input/train-v2.0_0_SL.html", "input/train-v2.0_1_SL.html",
    #                                          "input/train-v2.0_2_SL.html", "input/train-v2.0_3_SL.html"], "output")
