from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline, get_linear_schedule_with_warmup, AdamW, Trainer, TrainingArguments
from datasets import load_dataset
from torch.nn import functional as F
import json
import torch
# from sklearn.metrics import precision_recall_fscore_support, accuracy_score
from data_processing.reformat_squad_for_trainer import reformat_data
import subprocess
import os

# def compute_metrics(pred):
#     labels = pred.label_ids
#     preds = pred.predictions.argmax(-1)
#     precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
#     acc = accuracy_score(labels, preds)
#     return {
#         'accuracy': acc,
#         'f1': f1,
#         'precision': precision,
#         'recall': recall
#     }

def get_prediction(model_name, question, context):
    nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
    QA_input = {
        'question': question,
        'context': context
    }
    res = nlp(QA_input)
    print(res)

#get_prediction("deepset/xlm-roberta-large-squad2", 'Kdaj se je pojavila Frankovska identiteta?', "Normani (Norman: Nourmands; Francoščina: Normandi; Latinščina: Normanni) so bili ljudje, ki so v 10. in 11. stoletju dali ime Normandiji, regiji v Franciji. Bili so potomci nordijskih plenilcev in piratov iz Danske, Islandije in Norveške, ki so pod svojim voditeljem Rollom prisegli zvestobo kralju Karlu III. iz Zahodne Frankovske. Skozi generacije asimilacije in mešanja z domačimi frankovskimi in rimsko-gavskimi populacijami so se njihovi potomci postopoma združili s karolinškimi kulturami Zahodne Frankovske. Posebna kulturna in etnična identiteta Normanov se je sprva pojavila v prvi polovici 10. stoletja in se je razvijala v naslednjih stoletjih.")

def train_xlm_r(model_name):
    # with open('../data/train-v2.0.json', 'r') as f:
    #     train_data = json.load(f)
    #
    # train_data = [item for topic in train_data['data'] for item in topic['paragraphs']]
    #

    model = AutoModelForQuestionAnswering.from_pretrained(model_name, cache_dir="../cache")
    model.train()

    # We can use any PyTorch optimizer, but our library also provides the AdamW() optimizer which implements gradient bias correction as well as weight decay.
    # The optimizer allows us to apply different hyperpameters for specific parameter groups.
    # For example, we can apply weight decay to all parameters other than bias and layer normalization terms:

    no_decay = ['bias', 'LayerNorm.weight']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
         'weight_decay': 0.01},
        {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
    ]
    optimizer = AdamW(model.parameters(), lr=1e-5)

    # Now we can set up a simple dummy training batch using __call__().
    # This returns a BatchEncoding() instance which prepares everything we might need to pass to the model.

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    question, text = "Who was Jim Henson?", "Jim Henson was a nice puppet."
    encoding = tokenizer(question, text, return_tensors='pt')
    input_ids = encoding['input_ids']
    attention_mask = encoding['attention_mask']

    # When we call a classification model with the labels argument, the first returned element is the Cross Entropy loss
    # between the predictions and the passed labels.
    # Having already set up our optimizer, we can then do a backwards pass and update the weights:

    labels = torch.tensor([1, 0]).unsqueeze(0)
    outputs = model(input_ids, attention_mask=attention_mask)
    loss = F.cross_entropy(labels, outputs[0])
    loss.backward()
    optimizer.step()

    # We also provide a few learning rate scheduling tools.
    # With the following, we can set up a scheduler which warms up for num_warmup_steps and then linearly decays to 0 by the end of training.

    # scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps, num_train_steps)
    # scheduler.step()


def trainer(model_name):
    # train_data = reformat_data('../data/train-v2.0.json')
    # dev_data = reformat_data('../data/dev-v2.0.json')
    # dev_data_translated = reformat_data('../data_processing/output/dev-v2.0_translated_corrected.json')

    dataset = load_dataset('json',
                           data_files={'train': '../data_processing/output/reformated_train-v2.0.json',
                                       'validation': '../data_processing/output/reformated_dev-v2.0.json'},
                           field="data",
                           cache_dir="../data/reformated/train_eng")
    print(dataset)

    # model = AutoModelForQuestionAnswering.from_pretrained(model_name, cache_dir="../cache")
    # tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir="../cache")
    # training_args = TrainingArguments(
    #     output_dir='./results',  # output directory
    #     num_train_epochs=2,  # total # of training epochs
    #     per_device_train_batch_size=16,  # batch size per device during training
    #     per_device_eval_batch_size=64,  # batch size for evaluation
    #     warmup_steps=500,  # number of warmup steps for learning rate scheduler
    #     weight_decay=0.01,  # strength of weight decay
    #     logging_dir='./logs',  # directory for storing logs
    # )
    #
    # trainer = Trainer(
    #     model=model,  # the instantiated 🤗 Transformers model to be trained
    #     args=training_args,  # training arguments, defined above
    #     train_dataset=train_data,  # training dataset
    #     eval_dataset=dev_data,  # evaluation dataset
    #    # compute_metrics = compute_metrics()
    # )
    # trainer.train()
    # trainer.evaluate()

def eval(virtual_env, model_name):
    pr = subprocess.Popen([virtual_env, './fine_tune_HF.py',
                           '--model_name_or_path', model_name,
                           '--cache_dir', '../cache',
                           '--validation_file', '../data_processing/output/reformated_dev-v2.0.json',
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

eval("D:\\Anaconda\\envs\\NLP_TeamJodka\\python.exe", "deepset/xlm-roberta-large-squad2")

#trainer("xlm-roberta-large")

