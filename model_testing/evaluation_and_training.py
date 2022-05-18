from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline, get_linear_schedule_with_warmup, AdamW, Trainer, TrainingArguments
import subprocess

def get_prediction(model_name, question, context):
    nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
    QA_input = {
        'question': question,
        'context': context
    }
    res = nlp(QA_input)
    print(res)

#get_prediction("deepset/xlm-roberta-large-squad2", 'Kdaj se je pojavila Frankovska identiteta?', "Normani (Norman: Nourmands; Francoščina: Normandi; Latinščina: Normanni) so bili ljudje, ki so v 10. in 11. stoletju dali ime Normandiji, regiji v Franciji. Bili so potomci nordijskih plenilcev in piratov iz Danske, Islandije in Norveške, ki so pod svojim voditeljem Rollom prisegli zvestobo kralju Karlu III. iz Zahodne Frankovske. Skozi generacije asimilacije in mešanja z domačimi frankovskimi in rimsko-gavskimi populacijami so se njihovi potomci postopoma združili s karolinškimi kulturami Zahodne Frankovske. Posebna kulturna in etnična identiteta Normanov se je sprva pojavila v prvi polovici 10. stoletja in se je razvijala v naslednjih stoletjih.")

def eval(virtual_env, model_name, data_path):
    pr = subprocess.Popen([virtual_env, './fine_tune_HF.py',
                           '--model_name_or_path', model_name,
                           '--cache_dir', '../cache',
                           '--validation_file', data_path,
                           '--do_eval',
                           '--output_dir', './eval/' + model_name + '/',
                           '--version_2_with_negative'
                           ])
    stdout, stderr = pr.communicate()


def fine_tune(virtual_env):
    pr = subprocess.Popen([virtual_env, './fine_tune_HF.py',
                           '--model_name_or_path', 'xlm-roberta-base',
                           # '--dataset_name', 'squad_v2',
                           '--cache_dir', '../cache',
                           # '--train_file', '../data_processing/output/reformated_train-v2.0.json',
                           '--validation_file', '../data_processing/output/reformated_dev-v2.0.json',
                           # '--do_train',
                           '--do_eval',
                           '--per_device_train_batch_size', '4',
                           '--learning_rate', '3e-5',
                           '--num_train_epochs', '2',
                           '--max_seq_length', '320',
                           '--doc_stride', '128',
                           '--output_dir', './eval/debug_squad_v2/',
                           '--version_2_with_negative'
                           ])

    # pr = subprocess.Popen([virtual_env, './fine_tune_HF.py',
    #                        '--help',
    #                        ])
    stdout, stderr = pr.communicate()
    print(stdout)
    print(stderr)

# fine_tune("D:\\Anaconda\\envs\\NLP_TeamJodka\\python.exe")
# train_xlm_r("deepset/xlm-roberta-large-squad2")
# a-ware/xlmroberta-squadv2
# sontn122/xlm-roberta-large-finetuned-squad-v2

# eval("D:\\Anaconda\\envs\\NLP_TeamJodka\\python.exe", "deepset/xlm-roberta-large-squad2", "../data_processing/output/prevod_meta.json")
eval("G:\\NLP\\NLP_TeamJodka\\venv\\Scripts\\python.exe", "bert-base-multilingual-cased", "../data_processing/output/prevod_meta.json")

#trainer("xlm-roberta-large")

