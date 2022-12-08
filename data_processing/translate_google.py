import argparse
import os
import re
from pathlib import Path

from tqdm import tqdm

from google.cloud import translate
from google.cloud import storage


def correct_formatting(file_path, output_file_path):
    def add_parenthesis(match_obj):
        number = match_obj.string[match_obj.span()[0] + 1:match_obj.span()[1] - 1]
        return f'="{number}">'

    def add_newline(match_obj):
        tag = match_obj.string[match_obj.span()[0]:match_obj.span()[1]]
        tag.strip()
        tag = re.sub(r'=\d+>', add_parenthesis, tag)
        return tag + "\n"

    with open(file_path, encoding="utf-8") as f:
        content = f.read()
        content = content.replace("\n", "")
        pattern = re.compile(r'(<data class=\d+>\s*)|(</data>\s*)|'
                             r'(<paragraph class=\d+>\s*)|(</paragraph>\s*)|'
                             r'(</context>\s*)|'
                             r'(<qas class=\d+>\s*)|(</qas>\s*)|'
                             r'(</question>\s*)|'
                             r'(<answer class=\d+>\s*)|(</answer>\s*)|'
                             r'(<plausible_answer class=\d+>\s*)|(</plausible_answer>\s*)|'
                             r'(</text>\s*)|'
                             r'(</in_context>\s*)')
        content = re.sub(pattern, add_newline, content)
        with open(output_file_path, "w", encoding="utf-8") as o:
            o.write(content)


def init_bucket(bucket_name):
    storage_client = storage.Client()
    return storage_client, storage_client.bucket(bucket_name)


def upload_blob(source_file_name, destination_blob_name, bucket=None, bucket_name=None):
    if bucket is None:
        _, bucket = init_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


def rename_blob(blob_name, new_name, bucket=None, bucket_name=None):
    if bucket is None:
        _, bucket = init_bucket(bucket_name)
    # blob_name = f"gs://{blob_name}"
    print(blob_name)
    blob = bucket.blob(blob_name)

    new_blob = bucket.rename_blob(blob, new_name)

    print(f"Blob {blob.name} has been renamed to {new_blob.name}")


def download_blob(source_blob_name, destination_file_name, bucket=None, bucket_name=None):
    if bucket is None:
        _, bucket = init_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(f"Downloaded storage object {source_blob_name} to local file {destination_file_name}.")


def batch_translate_text(
        file_name,
        input_folder_path,
        output_folder_path,
        project_id,
        storage_id,
        timeout=3600,
        client=None
):
    input_uri = f"gs://{storage_id}/{input_folder_path}/{file_name}"  # train-v2.0_0.html
    output_uri = f"gs://{storage_id}/{output_folder_path}/{file_name}/"

    """Translates a batch of texts on GCS and stores the result in a GCS location."""
    if client is None:
        client = translate.TranslationServiceClient()

    location = "us-central1"
    # Supported file types: https://cloud.google.com/translate/docs/supported-formats
    gcs_source = {"input_uri": input_uri}

    input_configs_element = {
        "gcs_source": gcs_source,
        "mime_type": "text/html",  # Can be "text/plain" or "text/html".
    }
    gcs_destination = {"output_uri_prefix": output_uri}
    output_config = {"gcs_destination": gcs_destination}
    parent = f"projects/{project_id}/locations/{location}"

    # Supported language codes: https://cloud.google.com/translate/docs/languages
    operation = client.batch_translate_text(
        request={
            "parent": parent,
            "source_language_code": "en",
            "target_language_codes": ["sl"],  # Up to 10 language codes here.
            "input_configs": [input_configs_element],
            "output_config": output_config,
        }
    )

    print("Translation in progress...")
    response = operation.result(timeout)

    print("Total Characters: {}".format(response.total_characters))
    print("Translated Characters: {}".format(response.translated_characters))


def translate_with_google(input_folder, base_name, cloud_folder="train", cloud_folder_output="results/train",
                          bucket_name="train-nlp-journal", project_id="nlp-journal", check_files=True):
    storage_client, bucket = init_bucket(bucket_name)
    client = translate.TranslationServiceClient()
    file_list = [f for f in os.listdir(input_folder) if re.search(r'^' + base_name + '_\d+.html$', f)]
    file_list = sorted(file_list, key=lambda s: int(re.findall(r'\d+', s)[2]))
    for i, file in enumerate(file_list):
        print(f"Current file ({i}/{len(file_list)}): {file}")
        destination_file_path = f"{cloud_folder}/{file}"
        if check_files:
            file_path = f"{input_folder}/{file}"
            if not storage.Blob(bucket=bucket, name=destination_file_path).exists(storage_client):
                upload_blob(file_path, destination_file_path, bucket=bucket)
            else:
                print(f"Already uploaded.")

        if not storage.Blob(bucket=bucket, name=f"{cloud_folder_output}/{file}/index.csv").exists(storage_client):
            batch_translate_text(file_name=file, input_folder_path=cloud_folder, output_folder_path=cloud_folder_output,
                                 client=client, project_id=project_id, storage_id=bucket_name)
        else:
            print("Already translated.")

        result_file = f"{cloud_folder_output}/{file}/{bucket_name}_{cloud_folder}_{Path(file).stem}" \
                      f"_sl_translations.html"
        local_file = f"input/train_translated/google_unformatted/{Path(file).stem}_SL.html"
        formatted_file = f"input/train_translated/google/{Path(file).stem}_SL.html"
        if not os.path.isfile(local_file) and not os.path.isfile(formatted_file):
            download_blob(result_file, local_file, bucket=bucket)
        else:
            print("Already downloaded.")

        if not os.path.isfile(formatted_file):
            correct_formatting(local_file, formatted_file)
        else:
            print("Already formatted.")

def correct_files(input_folder, base_name):
    file_list = [f for f in os.listdir(input_folder) if re.search(r'^' + base_name + '_\d+.html$', f)]
    file_list = sorted(file_list, key=lambda s: int(re.findall(r'\d+', s)[2]))
    for i, file in enumerate(file_list):
        print(f"Current file ({i}/{len(file_list)}): {file}")
        local_file = f"input/train_translated/google_unformatted/{Path(file).stem}_SL.html"
        formatted_file = f"input/train_translated/google/{Path(file).stem}_SL.html"
        if not os.path.isfile(formatted_file):
            correct_formatting(local_file, formatted_file)
        else:
            print("Already formatted.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input folder.", required=True)
    parser.add_argument("-f", "--filename", help="Base file name.", required=True)
    parser.add_argument("-cf", "--cloud_folder", help="Input folder on cloud.", required=True)
    parser.add_argument("-co", "--cloud_folder_output", help="Output folder on cloud.", required=True)
    parser.add_argument("-b", "--bucket_name", help="Cloud bucket name.", required=True)
    parser.add_argument("-p", "--project_id", help="Project name.", required=True)
    parser.add_argument("-check", "--check_files", default=True, type=bool,
                        help="Whether to upload files if they don't exist on cloud before translating.")
    parser.add_argument("--correct_only", default=False, type=bool,
                        help="Whether to only correct existing files.")
    args = parser.parse_args()
    print(args)
    if not args.correct_only:
        translate_with_google(args.input, args.filename, args.cloud_folder, args.cloud_folder_output,
                              args.bucket_name, args.project_id, args.check_files)
    else:
        correct_files(args.input, args.filename)
    # translate_with_google("output/train_html", "train-v2.0", check_files=False)
