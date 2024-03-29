import glob
import json
import copy
import os
import re
import argparse

def build_json_with_context(input_english_json, input_translated_html, output_path, answer_tag="b"):
    with open(input_english_json, encoding="utf8") as f:
        json_english = json.load(f)

    json_output = copy.deepcopy(json_english)

    def get_order(file):
        g = re.findall(r'.*_(\d+)_.*', file)
        return int(g[0])

    if os.path.isdir(input_translated_html):
        input_translated_html = sorted(glob.glob(os.path.join(input_translated_html, '*.html')), key=get_order)
    elif not isinstance(input_translated_html, list):
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

                index = line.find(f"<{answer_tag} class='answer'>")
                json_output["data"][indexes["data"]]["paragraphs"][indexes["paragraph"]]["qas"][indexes["qas"]][
                    answer_type + "s"][indexes[answer_type]]["answer_start"] = index

                json_output["data"][indexes["data"]]["paragraphs"][indexes["paragraph"]]["qas"][indexes["qas"]][
                    answer_type + "s"][indexes[answer_type]]["text_in_context"] = line

                line = (line.split(f"<{answer_tag} class='answer'>")[1].split(f"</{answer_tag}>"))[0]
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
    # output_file_name = Path(input_english_json).stem
    if not output_path.endswith(".json"):
        output_path += ".json"
    with open(output_path, "w", encoding="utf8") as f:
        f.write(json.dumps(json_output, ensure_ascii=False))


if __name__ == '__main__':
    # build_json_with_context("../data/train-v2.0.json", "input/train_translated", "output")
    # json_to_html("../data/dev-v2.0.json", ["input/dev-v2.0_0_SL.html", "input/dev-v2.0_1_SL.html",
    #                                        "input/dev-v2.0_2_SL.html"], "output")
    # json_to_html("../data/train-v2.0.json", ["input/train-v2.0_0_SL.html", "input/train-v2.0_1_SL.html",
    #                                          "input/train-v2.0_2_SL.html", "input/train-v2.0_3_SL.html"], "output")

    parser = argparse.ArgumentParser()
    parser.add_argument("-ie", "--input_english", help="Input english (JSON).", required=True)
    parser.add_argument("-it", "--input_translated", help="Directory with translated html files.", required=True)
    parser.add_argument("-o", "--output", help="Output file.", required=True)
    parser.add_argument("-t", "--tag", help="HTML tag denoting the answer.", default="b")
    args = parser.parse_args()
    print(args)
    build_json_with_context(args.input_english, args.input_translated, args.output, args.tag)
