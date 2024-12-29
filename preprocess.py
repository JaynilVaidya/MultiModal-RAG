import json
from extract import ExtractText
from multiprocessing import Process, Queue, Manager, Lock
from sentence_transformers import SentenceTransformer
import faiss
from glob import glob
import numpy as np
import os

def extractor(fpQueue, dataQueue, extract_text, metadata_file, index_counter, lock):
    print("Starting Extractor")
    while not fpQueue.empty():
        try:
            filepath = fpQueue.get(block=False)
            print(f"Extracting text from {filepath}")
            for metadata in extract_text.extract_text(filepath):
                with lock:
                    index = index_counter.value
                    index_counter.value += 1
                    with open(metadata_file, 'r') as f:
                        try:
                            all_metadata = json.load(f)
                        except Exception as e:
                            print(e)
                            continue
                    all_metadata["corpus"][index] = metadata
                    with open(metadata_file, 'w') as f: json.dump(all_metadata, f, indent=4)
                
                dataQueue.put((index, metadata['content']))
        except Exception as e:
            print(e)
            print('### Stopping Extractor ###')
            break

def embedder(dataQueue, embeddings_list):
    print("Starting Embedder")
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    
    while True:
        try:
            index, content = dataQueue.get(block=True, timeout=10)
            print(f"Embedding data from index {index}")
            embeddings = embedding_model.encode(content, convert_to_numpy=True, show_progress_bar=True)
            embeddings_list.append((index, embeddings))
        except Exception as e:
            print(e)
            print('### Stopping Embedder ###')
            break

class Preprocess:
    def __init__(self, folderpath):
        self.extract_text = ExtractText()
        self.folderpath = folderpath
        self.dataQueue = Queue()
        self.fpQueue = Queue()
        self.manager = Manager()
        self.embeddings_list = self.manager.list()
        self.index_counter = self.manager.Value('i', 0)
        self.lock = Lock()
        self.metadata_file = 'metadata.json'
        
        with open(self.metadata_file, 'w') as f: json.dump({"corpus": {}}, f, indent=4)
        
        self.filepaths = glob(f"{self.folderpath}/*")
        for fp in self.filepaths: self.fpQueue.put(fp)
        
        print(f'Total Number of files: {len(self.filepaths)}')
        
    def start_parallel(self):
        extractor_processes = [Process(target=extractor, args=(self.fpQueue, self.dataQueue, self.extract_text, self.metadata_file, self.index_counter, self.lock)) for _ in range(3)]
        embedder_processes = [Process(target=embedder, args=(self.dataQueue, self.embeddings_list)) for _ in range(2)]
        
        print("Starting Parallel-Preprocessing")
        for p in extractor_processes + embedder_processes: p.start()
        
        for p in extractor_processes + embedder_processes: p.join()
        
        print("Parallel-Preprocessing completed!")
        
        # Combine embeddings in the main process
        embeddings_index = faiss.IndexFlatL2(384)
        for index, embeddings in self.embeddings_list:
            embeddings = np.array(embeddings).reshape(1, -1)
            embeddings_index.add(embeddings)
        
        print("All embeddings added to the FAISS index.")
        return embeddings_index

if __name__ == "__main__":
    folderpath = r"C:\Users\Jaynil\LLMs\content"
    pre = Preprocess(folderpath)
    pre.start_parallel()
