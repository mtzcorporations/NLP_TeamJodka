# Cross-lingual question answering
### Matjaž Zupanič, Maj Zirkelbach, Uroš Šmajdek and Meta Jazbinšek
##### Joint project between Faculty of Computer and Information Science and Faculty of Arts Faculty, University of Ljubljana

## Installation

### Dependencies 
- Python 3
- [PyTorch](https://pytorch.org/) (currently tested on version 1.7.0)

### Quick installation
```bash
pip install -r requirements.txt
```

## Introduction
Context-based question  answering is the task of finding an answer to a question over a given context.
	Machine question answering is an essential yet challenging task in natural language processing. Recently, pre-trained Contextual Embeddings (PCE) models like [Bidirectional Encoder Representations from Transformers (BERT)](https://arxiv.org/abs/1810.04805) and [A Lite BERT (ALBERT)](https://arxiv.org/pdf/1909.11942.pdf) have attracted lots of attention due to their great performance in a wide range of NLP tasks.

### Project Instructions
Students will jointly work on dataset preparation and then use multilingual models for English and Slovene corpora. They will check the performance of transfer learning for question answering from English to Slovene. The results will be compared with the Slovene-only model, trained on translated data.


The UL FRI students will use [EK translator](https://ec.europa.eu/cefdigital/wiki/display/CEFDIGITAL/eTranslation) to translate corpora (SQuAD 2.0, ReaddleSense), then UL FF students will manually check and correct corpus. The corpus will need to be carefully prepared as it will be merged together from all the groups and used for the analysis. Corpus will also need to be published to Clarin.si repository.


The UL FRI are expected to set up and help UL FF students with the "translation platform - e.g., Memsource." Then they will build models (transfer learning, multi-lingual models, Slovene-only models) and do analyses, evaluation. Both students are supposed to work together on the discussion part.

## Datasets

TODO

## Results

TODO