# Cross-Lingual Question Answering
### Matjaž Zupanič, Maj Zirkelbach, Uroš Šmajdek and Meta Jazbinšek
##### Joint project between Faculty of Computer and Information Science and Faculty of Arts, University of Ljubljana

# Table of Contents
1. [Installation](#Installation)
2. [Usage](#Usage)
3. [Introduction](#Introduction)
4. [Datasets](#Datasets)
5. [Models](#Models)

## Installation

### Dependencies 
- Python 3
- [PyTorch](https://pytorch.org/) (currently tested on version 1.11.0)
- [Transformers](https://github.com/huggingface/transformers) (currently tested on version 4.19.0.dev0)

### Quick installation
```bash
pip install -r requirements.txt
```

## Usage

#### Model Evaluation
*The below will evaluate RemBERT on Slovene machine translated dataset localed in data folder.*
```bash
python training_and_evaluation/fine_tune_HF.py --do_eval --model_name_or_path Sindhu/rembert-squad2 --validation_file data/rf_dev-v2.0_SLO_translated_corrected.json --output_dir output/rembert --version_2_with_negative
```

#### Fine-Tuning
*The below will fine-tune M-BERT-base model, located in models folder, on Slovene machine translated dataset localed in data folder.*

```bash
python training_and_evaluation/fine_tune_HF.py --do_train --model_name_or_path models/mBertBase_ENG --train_file data/rf_train-v2.0_SLO_translated_corrected.json --validation_file data/rf_dev-v2.0_SLO_translated_corrected.json --per_device_train_batch_size 4 --learning_rate 3e-5 --num_train_epochs 3 --max_seq_length 320 --output_dir results/fine_tuning--version_2_with_negative
```

#### List additional parameters and their descriptions
```bash
python training_and_evaluation/fine_tune_HF.py -h
```

## Introduction
A core goal in artificial intelligence is to build systems that can read the web, and then answer complex questions about any topic over given content. These question-answering (QA) systems could have a big impact on the way that we access information. Furthermore, open-domain question answering is a benchmark task in the development of Artificial Intelligence, since understanding text and being able to answer questions about it is something that we generally associate with intelligence.
  
Recently, pre-trained Contextual Embeddings (PCE) models like Bidirectional Encoder Representations from Transformers [Bidirectional Encoder Representations from Transformers (BERT)](https://arxiv.org/abs/1810.04805) and [A Lite BERT (ALBERT)](https://arxiv.org/pdf/1909.11942.pdf) have attracted lots of attention due to their great performance in a wide range of NLP tasks.
	
Multilingual question answering tasks typically assume that answers exist in the same language as the question. Yet in practice, many languages face both information scarcity—where languages have few reference articles—and information asymmetry—where questions reference concepts from other cultures. Due to the sizes of modern corpora, performing human translations is generally infeasible, therefore we often employ machine translations instead. Machine translation however, is for the most part incapable of interpreting nuances of specific languages, especially when translating between different language groups.
	
In this work we present a method for a construct of a machine translated dataset from [SQuAD 2.0](https://arxiv.org/abs/1806.03822) and evaluate its quality using various modern QA models. Additionally, we benchmark its effectiveness by performing a manual post editing on a subset of the translated dataset and comparing the results.

### Project Instructions
Students will jointly work on dataset preparation and then use multilingual models for English and Slovene corpora. They will check the performance of transfer learning for question answering from English to Slovene. The results will be compared with the Slovene-only model, trained on translated data.


The UL FRI students will use [EK translator](https://ec.europa.eu/cefdigital/wiki/display/CEFDIGITAL/eTranslation) to translate corpora (SQuAD 2.0, ReaddleSense), then UL FF students will manually check and correct corpus. The corpus will need to be carefully prepared as it will be merged together from all the groups and used for the analysis. Corpus will also need to be published to Clarin.si repository.


The UL FRI are expected to set up and help UL FF students with the "translation platform - e.g., Memsource." Then they will build models (transfer learning, multi-lingual models, Slovene-only models) and do analyses, evaluation. Both students are supposed to work together on the discussion part.

## Datasets

SQuAD 2.0 [Train](https://drive.google.com/file/d/1q_uHuOCBPMko7ljsb9vYroEPDSC8Hsa_/view?usp=sharing) [Test](https://drive.google.com/file/d/1uzm6TjfB3xy6G78kwx5F3d0yeaTRNkTV/view?usp=sharing) ([Website](https://rajpurkar.github.io/SQuAD-explorer/)) \
Machine Translated SQuAD 2.0 [Train](https://drive.google.com/file/d/1Fc3iOQaGRzPnQ68zh3Weieu4qnTETre-/view?usp=sharing) [Test](https://drive.google.com/file/d/1h_-v5OI_gMRnH4pl0Zx0rnirZnm0keVb/view?usp=sharing) \
[Human Translated subset of SQuAD 2.0](https://drive.google.com/file/d/1y_LYKDX3norDSHp9KUuMR6e1ZSc-nhyv/view?usp=sharing) ([English](https://drive.google.com/file/d/17z7CYztCUP6Wp1GYretrQCTQ6Cjv3QG3/view?usp=sharing) and [Machine Translated](https://drive.google.com/file/d/18xDbzfJAGQPgdPTMbyLnWb4iyAUO7HLP/view?usp=sharing) counterparts)

## Pre-Trained Models

| Model Name   | ENG                                                                                                | SLO          | ENG & SLO                                                                                          |
|--------------|----------------------------------------------------------------------------------------------------|--------------|----------------------------------------------------------------------------------------------------|
| M-BERT       | [Google Drive](https://drive.google.com/file/d/1KidXu1eG38K5Z8AU7aTNlJzyrnXaV5Sh/view?usp=sharing) | [Google Drive](https://drive.google.com/file/d/17c2TMw21hF1yllCbi-n_t_St7BAURuml/view?usp=sharing) | [Google Drive](https://drive.google.com/file/d/1TGp2pisgQwBN5tsulqRIluuKwipehjsG/view?usp=sharing) |
| xlm-R        | [Huggingface](https://huggingface.co/deepset/xlm-roberta-large-squad2)                             | [Google Drive](https://drive.google.com/file/d/1PlRISTHd9nakEabQt41MjrRTSLm7Cw9W/view?usp=sharing) | [Google Drive](https://drive.google.com/file/d/13DsJFW-4UcQQ3MvHPlkBEd2O3wFz1n15/view?usp=sharing) |
| RemBERT      | [Huggingface](https://huggingface.co/Sindhu/rembert-squad2)                                                                                    | -            | -                                                                                                  |
| CroSloEngual | [Google Drive](https://drive.google.com/file/d/1SoHUNIs5riY_KlnXMlPwlbz0rXD4aVhb/view?usp=sharing)                                                                                       | [Google Drive](https://drive.google.com/file/d/1PDAq5ZSmCjKudcictyiA01huAxs-zY4K/view?usp=sharing) | [Google Drive](https://drive.google.com/file/d/1lTh9xi5-dXjP6iCl_RzEZgflUoA8soq3/view?usp=sharing) |
| SloBERTa     | -                                                                                                  | -            | [Google Drive](https://drive.google.com/file/d/1Pz9bZEwWlAZ75Qexlg2tu9C_Rri-kSU0/view?usp=sharing)                                                                                   |