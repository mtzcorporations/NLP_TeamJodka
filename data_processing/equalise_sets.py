import json
import os
import argparse
import copy


def equalise_sets(input_translated, input_english, output_path):
    with open(input_translated, encoding="utf8") as f:
        dataset = json.load(f)
    with open(input_english, encoding="utf8") as f:
        dataset_english = json.load(f)
    dataset_english_2 = copy.deepcopy(dataset_english)
    dataset_output = {"version": dataset_english["version"], "data": []}
    all_questions = 0
    correct_questions = 0

    for d_i, document in enumerate(dataset["data"]):
        english_document = None
        for p_i, paragraph in enumerate(document["paragraphs"]):
            english_paragraph = None
            for q_i, qas in enumerate(paragraph["qas"]):
                all_questions += 1
                english_question = None
                answer_type = "answers"
                if qas["is_impossible"]:
                    answer_type = "plausible_answers"
                correct_question = False
                for pa_i, answer in enumerate(qas[answer_type]):
                    if qas["is_impossible"] or answer["answer_start"] != -1:
                        correct_question = True
                    if english_document is None:
                        english_document = {"title": dataset_english["data"][d_i]["title"], "paragraphs": []}
                        dataset_output["data"].append(english_document)
                    if english_paragraph is None:
                        english_paragraph = {"context": dataset_english["data"][d_i]["paragraphs"][p_i][
                            "context"], "qas": []}
                        english_document["paragraphs"].append(english_paragraph)
                    if english_question is None:
                        english_question = {"question": dataset_english["data"][d_i]["paragraphs"][p_i]["qas"]
                            [q_i]["question"], "id": qas["id"], "is_impossible": qas["is_impossible"], answer_type: []}
                        if qas["is_impossible"]:
                            english_question["answers"] = []
                        english_paragraph["qas"].append(english_question)
                    english_question[answer_type].append(
                        dataset_english["data"][d_i]["paragraphs"][p_i]["qas"][q_i][answer_type][pa_i])
                    if not qas["is_impossible"] and answer["answer_start"] == -1:
                        english_question[answer_type][-1]["answer_start"] = -1

                if not correct_question:
                    correct_question = True
                    for answer in dataset_english_2["data"][d_i]["paragraphs"][p_i]["qas"][q_i][answer_type]:
                        if answer["answer_start"] != -1:
                            correct_question = False
                            break
                if correct_question:
                    correct_questions += 1

    print(f'% of all questions: {(correct_questions / all_questions):.4f}')
    with open(os.path.join(output_path), "w", encoding="utf8") as f:
        f.write(json.dumps(dataset_output, ensure_ascii=False))


if __name__ == '__main__':
    # equalise_sets("output/train-v2.0_translated_corrected.json", "../data/train-v2.0.json",
    #               "output/train-v2.0_normalized.json")

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--input_reference", help="Reference file.", required=True)
    parser.add_argument("-i", "--input", help="Input file.", required=True)
    parser.add_argument("-o", "--output", help="Output file.", required=True)
    args = parser.parse_args()
    print(args)
    equalise_sets(args.input_reference, args.input, args.output)


