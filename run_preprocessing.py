from preprocess import Preprocess
from extract import ExtractText
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import json

#%% running preprocessor
if __name__ == "__main__":
    folderpath = r"C:\Users\Jaynil\LLMs\content"
    pre = Preprocess(folderpath)
    emixs = pre.start_parallel()
    faiss.write_index(emixs, "my_faiss_index.index")
    print(emixs)