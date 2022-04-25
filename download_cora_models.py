import urllib.request

def download_models():
    urllib.request.urlretrieve("https://nlp.cs.washington.edu/xorqa/cora/models/all_w100.tsv", "./models/all_w100.tsv")
    urllib.request.urlretrieve("https://nlp.cs.washington.edu/xorqa/cora/models/mGEN_model.zip", "./models/mGEN_model.zip")
    urllib.request.urlretrieve("https://nlp.cs.washington.edu/xorqa/cora/models/mDPR_biencoder_best.cpt", "./models/mDPR_biencoder_best.cpt")

    for i in ["0", "1", "2", "3", "4", "5", "6", "7"]:
        urllib.request.urlretrieve("https://nlp.cs.washington.edu/xorqa/cora/models/wikipedia_split/wiki_emb_en_" + i, "./models/embeddings/wiki_emb_en_" + i)

    for i in ["0", "1", "2", "3", "4", "5", "6", "7"]:
        urllib.request.urlretrieve("https://nlp.cs.washington.edu/xorqa/cora/models/wikipedia_split/wiki_emb_others_" + i, "./models/embeddings/wiki_emb_others_" + i)

#download_models()