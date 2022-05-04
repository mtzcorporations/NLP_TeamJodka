import json
import os
from pathlib import Path
from tqdm import tqdm

global file_index, current_file

MAX_FILE_SIZE = 4
ANSWER_TAG = "b"

def check_file_size(input_path, output_path):
    global file_index, current_file
    if current_file.tell() / 1000000 > MAX_FILE_SIZE:
        file_index += 1
        current_file.close()
        current_file = open(os.path.join(output_path, Path(input_path).stem + f"_{file_index}.html"), "w",
                            encoding="utf-8")


def write_tag(tag, input_path, output_path, opened=True, index=-1):
    check_file_size(input_path, output_path)
    if opened:
        current_file.write(f"<{tag} class={index}>\n")
    else:
        current_file.write(f"</{tag}>\n")


def write_text(tag, text, input_path, output_path):
    check_file_size(input_path, output_path)
    current_file.write(f"<{tag}>{str(str(text))}</{tag}>\n")


def json_to_html(input_path, output_path):
    global file_index, current_file
    with open(input_path, encoding="utf-8") as f:
        dataset = json.load(f)
    file_index = 0
    current_file = open(os.path.join(output_path, Path(input_path).stem + f"_{file_index}.html"), "w", encoding="utf-8")

    for d_i, document in enumerate(tqdm(dataset["data"])):
        write_tag("data", input_path, output_path, True, d_i)
        for p_i, paragraph in enumerate(document["paragraphs"]):
            write_tag("paragraph", input_path, output_path, True, p_i)
            context = paragraph["context"]
            write_text("context", context, input_path, output_path)
            for q_i, qas in enumerate(paragraph["qas"]):
                write_tag("qas", input_path, output_path, True, q_i)
                write_text("question", qas["question"], input_path, output_path)

                if "plausible_answers" in qas:
                    for pa_i, plausible_answer in enumerate(qas["plausible_answers"]):
                        answer_start = plausible_answer["answer_start"]
                        answer_end = answer_start + len(plausible_answer["text"])
                        answer_in_context = f"{context[:answer_start]}<{ANSWER_TAG} class='answer'>" \
                                            f"{context[answer_start:answer_end]}</{ANSWER_TAG}>{context[answer_end:]}"

                        write_tag("plausible_answer", input_path, output_path, True, pa_i)
                        write_text("text", plausible_answer["text"], input_path, output_path)
                        write_text("in_context", answer_in_context, input_path, output_path)
                        write_tag("plausible_answer", input_path, output_path, False, pa_i)

                if "answers" in qas:
                    for a_i, answer in enumerate(qas["answers"]):
                        answer_start = answer["answer_start"]
                        answer_end = answer_start + len(answer["text"])
                        answer_in_context = f"{context[:answer_start]}<{ANSWER_TAG} class='answer'>" \
                                            f"{context[answer_start:answer_end]}</{ANSWER_TAG}>{context[answer_end:]}"

                        write_tag("answer", input_path, output_path, True, a_i)
                        # write_text("text", answer["text"], input_path, output_path)
                        write_text("in_context", answer_in_context, input_path, output_path)
                        write_tag("answer", input_path, output_path, False, a_i)

                write_tag("qas", input_path, output_path, False, q_i)
            write_tag("paragraph", input_path, output_path, False, p_i)
        write_tag("data", input_path, output_path, False, d_i)

    current_file.close()


if __name__ == '__main__':
    json_to_html("../data/train-v2.0.json", "output")
