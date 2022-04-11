import json
import os
from pathlib import Path

global file_index, current_file


def json_to_html(input_path, output_path):
    global file_index, current_file
    with open(input_path, encoding="utf-8") as f:
        file = json.load(f)
    dataset = file["data"]
    file_index = 0
    current_file = open(os.path.join(output_path, Path(input_path).stem + f"_{file_index}.html"), "w", encoding="utf-8")
    json_to_html_write_element("data", dataset, input_path, output_path)
    current_file.close()


def json_to_html_write_element(key, value, input_path, output_path):
    global file_index, current_file
    # Max file size for translation is 20MB, so we split the files into max 18MB chunks
    if current_file.tell() / 1000000 > 15:
        file_index += 1
        current_file.close()
        current_file = open(os.path.join(output_path, Path(input_path).stem + f"_{file_index}.html"), "w",
                            encoding="utf-8")

    if isinstance(value, list):
        for i, val in enumerate(value):
            json_to_html_write_element(key + "_" + str(i), val, input_path, output_path)
    elif isinstance(value, dict):
        current_file.write(f"<{key}>\n")
        for k, val in value.items():
            json_to_html_write_element(k, val, input_path, output_path)
        current_file.write(f"</{key}>\n")
    else:
        current_file.write(f"<{key}>{str(value)}</{key}>\n")


if __name__ == '__main__':
    json_to_html("../data/train-v2.0.json", "output")
