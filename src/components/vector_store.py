import os
import sys
from dataclasses import dataclass
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object, save_vector_store # Ab ye modular hai!

@dataclass
class VectorStoreConfig:
    vector_db_path: str = os.path.join('artifacts', "faiss_index")

class VectorStore:
    def __init__(self):
        self.vector_config = VectorStoreConfig()
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def initiate_vector_store(self, chunks_file_path):
        try:
            logging.info("Loading chunks using modular utils...")
           
            chunks = load_object(file_path=chunks_file_path)
            
            logging.info(f"Creating Embeddings for {len(chunks)} chunks...")
            vector_db = FAISS.from_texts(texts=chunks, embedding=self.embeddings)
            
           
            logging.info("Saving Vector Store via Utils...")
            save_vector_store(
                folder_path=self.vector_config.vector_db_path,
                vector_store_obj=vector_db
            )

            return self.vector_config.vector_db_path

        except Exception as e:
            raise CustomException(e, sys)

