import classla
import json
import numpy as np
import os
from pathlib import Path
from tqdm import tqdm

def create_lemma_array(text, nlp):
    answer_processed = nlp(text)
    lemma_array = []
    for i, sentence in enumerate(answer_processed.sentences):
        for word in sentence.words:
            lemma_array.append(word)
    return np.array(lemma_array)


def correct_translation(input_translated, input_english, output_path, document_limit=-1):
    with open(input_translated, encoding="utf8") as f:
        dataset = json.load(f)
    with open(input_english, encoding="utf8") as f:
        dataset_english = json.load(f)

    classla.download('sl')
    nlp = classla.Pipeline('sl', processors='tokenize,ner,pos,lemma,depparse')

    if document_limit > 0:
        dataset["data"] = dataset["data"][:document_limit]

    total = 0
    correct = 0
    corrected = 0
    # enumerate(tqdm(document["paragraphs"], desc=f"Document {d_i}/{len(dataset['data'])}")):

    # Compute total answers:
    for document in dataset["data"]:
        for paragraph in document["paragraphs"]:
            for qas in paragraph["qas"]:
                total += len(qas["answers"])

    checked = 0
    log = open("correction.log", "w", encoding="utf8")
    with tqdm(total=total) as pbar:
        for d_i, document in enumerate(dataset["data"]):
            for p_i, paragraph in enumerate(document["paragraphs"]):
                doc_lemma_array = None
                for q_i, qas in enumerate(paragraph["qas"]):
                    for a_i, answer in enumerate(qas["answers"]):
                        checked += 1
                        if answer["answer_start"] != -1:
                            correct += 1
                            pbar.update(1)
                            pbar.set_description(f'Found: {((correct + corrected) / checked) * 100:.2f}%')
                            continue
                        if doc_lemma_array is None:
                            doc_lemma_array = create_lemma_array(paragraph["context"], nlp)

                        answer_lemma_array = create_lemma_array(answer["text"], nlp)
                        found = True
                        for i in range(len(doc_lemma_array) - len(answer_lemma_array) + 1):
                            found = True
                            for j in range(len(answer_lemma_array)):
                                if answer_lemma_array[j].lemma != doc_lemma_array[i + j].lemma:
                                    found = False
                                    break
                            if found:
                                corrected += 1
                                index = paragraph["context"].find(doc_lemma_array[i].text)
                                answer["answer_start"] = index
                                new_answer = []
                                for j in range(len(answer_lemma_array)):
                                    new_answer.append(doc_lemma_array[i + j].text)
                                answer["text"] = " ".join(new_answer)
                                answer["corrected"] = True
                                break
                        if not found:
                            log.write(
                                f'{dataset_english["data"][d_i]["paragraphs"][p_i]["qas"][q_i]["answers"][a_i]["text"]}'
                                f';'
                                f'{answer["text"]}\n')
                        pbar.update(1)
                        pbar.set_description(f'Found: {((correct + corrected) / checked) * 100:.2f}%')
    log.close()

    print(f"Found fraction: {((correct + corrected) / total):.2f}")
    print(f"Corrected fraction: {(corrected / total):.2f} | {corrected}")
    output_file_name = Path(input_translated).stem
    with open(os.path.join(output_path, output_file_name + "_corrected.json"), "w", encoding="utf8") as f:
        f.write(json.dumps(dataset, ensure_ascii=False))


if __name__ == '__main__':
    # correct_translation("output/train-v2.0_translated.json", "../data/train-v2.0.json", "output")
    correct_translation("output/dev-v2.0_translated_old.json", "../data/dev-v2.0.json", "output")
