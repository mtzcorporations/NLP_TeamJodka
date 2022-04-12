import json
import copy
import os
import re
from pathlib import Path

ANSWER_TAG = "b"

def json_to_html(input_english_json, input_translated_html, output_path):
    with open(input_english_json, encoding="utf8") as f:
        json_english = json.load(f)

    json_output = copy.deepcopy(json_english)

    if not isinstance(input_translated_html, list):
        input_translated_html = [input_translated_html]

    indexes = {}
    has_answer = True
    for input_html in input_translated_html:
        f = open(input_html, encoding="utf8")
        for line in f.readlines():
            line = line.replace("\n", "")
            if re.match(r'<[^/]* class="\d+">', line):
                line = line.replace("<", "").replace(">", "")
                line = line.rsplit(" class=", 1)
                if line[0] == "answer":
                    has_answer = True
                elif line[0] == "plausible_answer":
                    has_answer = False
                indexes[line[0]] = int(line[1].replace("\"", ""))
                continue
            if "<question>" in line:
                line = line.replace("<question>", "").replace("</question>", "")
                json_output["data"][indexes["data"]]["paragraphs"][indexes["paragraph"]]["qas"][indexes["qas"]][
                    "question"] = line
                continue
            if "<text>" in line:
                line = line.replace("<text>", "").replace("</text>", "")
                if has_answer:
                    answer_type = "answer"
                else:
                    answer_type = "plausible_answer"

                json_output["data"][indexes["data"]]["paragraphs"][indexes["paragraph"]]["qas"][indexes["qas"]][
                    answer_type + "s"][indexes[answer_type]]["text_basic"] = line
                continue
            if "<in_context>" in line:
                line = line.replace("<in_context>", "").replace("</in_context>", "")
                if has_answer:
                    answer_type = "answer"
                else:
                    answer_type = "plausible_answer"

                index = line.find(f"<{ANSWER_TAG} class='answer'>")
                json_output["data"][indexes["data"]]["paragraphs"][indexes["paragraph"]]["qas"][indexes["qas"]][
                    answer_type + "s"][indexes[answer_type]]["answer_start"] = index

                json_output["data"][indexes["data"]]["paragraphs"][indexes["paragraph"]]["qas"][indexes["qas"]][
                    answer_type + "s"][indexes[answer_type]]["text_in_context"] = line

                line = (line.split(f"<{ANSWER_TAG} class='answer'>")[1].split(f"</{ANSWER_TAG}>"))[0]
                json_output["data"][indexes["data"]]["paragraphs"][indexes["paragraph"]]["qas"][indexes["qas"]][
                    answer_type + "s"][indexes[answer_type]]["text"] = line
                continue
            if "<context>" in line:
                line = line.replace("<context>", "").replace("</context>", "")
                json_output["data"][indexes["data"]]["paragraphs"][indexes["paragraph"]]["context"] = line
        f.close()

    log = open("translation.log", "w", encoding="utf8")
    total = 0
    found = 0
    for d_i, document in enumerate(json_output["data"]):
        for p_i, paragraph in enumerate(document["paragraphs"]):
            for q_i, qas in enumerate(paragraph["qas"]):
                for a_i, answer in enumerate(qas["answers"]):
                    total += 1
                    index = paragraph["context"].find(answer["text"])
                    if index != -1:
                        found += 1
                    else:
                        json_output["data"][d_i]["paragraphs"][p_i]["qas"][q_i]["answers"][a_i]["answer_start"] = index
                        log.write(json_english["data"][d_i]["paragraphs"][p_i]["qas"][q_i]["answers"][a_i]["text"] +
                                  "\n" + answer["text"] + "\n" + answer["text_in_context"] + "\n" + paragraph[
                                      "context"] + "\n\n")
    log.close()
    print(f"Found fraction: {(found / total):.2f}")
    output_file_name = Path(input_english_json).stem
    with open(os.path.join(output_path, output_file_name + "_translated.json"), "w", encoding="utf8") as f:
        f.write(json.dumps(json_output, ensure_ascii=False))


if __name__ == '__main__':
    json_to_html("../data/dev-v2.0.json", ["input/dev-v2.0_0_SL.html", "input/dev-v2.0_1_SL.html",
                                           "input/dev-v2.0_2_SL.html"], "output")
    # json_to_html("../data/train-v2.0.json", ["input/train-v2.0_0_SL.html", "input/train-v2.0_1_SL.html",
    #                                          "input/train-v2.0_2_SL.html", "input/train-v2.0_3_SL.html"], "output")
