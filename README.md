# Multimodal Retrieval-Augmented Generation (RAG) Pipeline

This repository contains a Multimodal Retrieval-Augmented Generation (RAG) pipeline that processes various document formats, extracts text and images, and uses a language model to generate responses based on the retrieved context. The project leverages multiple Python libraries, including `PyPDF2`, `Pillow`, `faiss`, `sentence-transformers`, and `together`.

## Table of Contents

- [Introduction](#introduction)
- [Setup](#setup)
- [File Descriptions](#file-descriptions)
- [Usage](#usage)
- [Contributing](#contributing)

## Introduction

The Multimodal RAG pipeline is designed to handle documents in PDF, PPTX, TXT, and DOCX formats. It extracts text and images from these documents, processes them, and uses a language model to generate responses based on the retrieved context. The pipeline supports multimodal inputs, combining text and image data to provide more comprehensive responses. Additionally, the pipeline is parallelized to improve performance and uses FAISS for efficient similarity search.

## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```

2. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables:**

    Create a [.env](http://_vscodecontentref_/1) file in the root directory and add your Together API key:

    ```env
    TOGETHER_API_KEY=your_api_key_here
    ```

## File Descriptions

### [extract.py](http://_vscodecontentref_/2)

This file contains the `ExtractText` class, which is responsible for extracting text and images from various document formats. It includes methods for reading PDF, PPTX, TXT, and DOCX files, and processes the content into manageable chunks.

### [preprocess.py](http://_vscodecontentref_/3)

This file contains the `Preprocess` class, which orchestrates the parallel processing of documents. It uses multiprocessing to extract text and images, generate embeddings, and store metadata. The embeddings are indexed using FAISS for efficient similarity search.

### [run_preprocessing.py](http://_vscodecontentref_/4)

This script initializes the preprocessing pipeline and starts the parallel processing of documents. It saves the FAISS index to a file for later use.

### [helper.py](http://_vscodecontentref_/5)

This file contains helper functions for the project, including:
- `get_simcontext`: Retrieves similar contexts based on a query using the FAISS index.
- `interpret_image_with_context`: Sends images and context to the Together API for interpretation.

### [multimodelRAG.py](http://_vscodecontentref_/6)

This script demonstrates the RAG pipeline in action. It retrieves similar contexts based on a query, combines them, and uses the Together API to generate a response.

## Usage

1. **Run the preprocessing pipeline:**

    ```bash
    python run_preprocessing.py
    ```

    This will process the documents in the specified folder, generate embeddings, and save the FAISS index.

2. **Run the RAG pipeline:**

    ```bash
    python multimodelRAG.py
    ```

    This will retrieve similar contexts based on a query and generate a response using the Together API.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.
