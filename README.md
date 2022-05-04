# Cross-lingual question answering
### Matjaž Zupanič, Maj Zirkelbach, Uroš Šmajdek and Meta Jazbinšek
##### Joint project between Faculty of Computer and Information Science and Faculty of Arts, University of Ljubljana

## Installation

### Dependencies 
- Python 3
- [PyTorch](https://pytorch.org/) (currently tested on version 1.11.0)
- [Transformers](https://github.com/huggingface/transformers) (currently tested on version 4.19.0.dev0)

### Quick installation
```bash
pip install -r requirements.txt
```

## Introduction
A core goal in artificial intelligence is to build systems that can read the web, and then answer complex questions about any topic over given content. These question-answering (QA) systems could have a big impact on the way that we access information. Furthermore, open-domain question answering is a benchmark task in the development of Artificial Intelligence, since understanding text and being able to answer questions about it is something that we generally associate with intelligence.
  
Recently, pre-trained Contextual Embeddings (PCE) models like Bidirectional Encoder Representations from Transformers [Bidirectional Encoder Representations from Transformers (BERT)](https://arxiv.org/abs/1810.04805) and [A Lite BERT (ALBERT)](https://arxiv.org/pdf/1909.11942.pdf) have attracted lots of attention due to their great performance in a wide range of NLP tasks.
	
Multilingual question answering tasks typically assume that answers exist in the same language as the question. Yet in practice, many languages face both information scarcity—where languages have few reference articles—and information asymmetry—where questions reference concepts from other cultures. Due to the sizes of modern corpora, performing human translations is generally infeasible, therefore we often employ machine translations instead. Machine translation however, is for the most part incapable of interpreting nuances of specific languages, especially when translating between different language groups.
	
In our project we wish to evaluate various QA models on different types of corpora; original English variants, those machine translated into Slovene and those that were manually checked by a human after machine translation.

### Project Instructions
Students will jointly work on dataset preparation and then use multilingual models for English and Slovene corpora. They will check the performance of transfer learning for question answering from English to Slovene. The results will be compared with the Slovene-only model, trained on translated data.


The UL FRI students will use [EK translator](https://ec.europa.eu/cefdigital/wiki/display/CEFDIGITAL/eTranslation) to translate corpora (SQuAD 2.0, ReaddleSense), then UL FF students will manually check and correct corpus. The corpus will need to be carefully prepared as it will be merged together from all the groups and used for the analysis. Corpus will also need to be published to Clarin.si repository.


The UL FRI are expected to set up and help UL FF students with the "translation platform - e.g., Memsource." Then they will build models (transfer learning, multi-lingual models, Slovene-only models) and do analyses, evaluation. Both students are supposed to work together on the discussion part.

## Datasets

TODO

## Results

TODO
