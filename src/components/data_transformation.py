import os
import sys
from dataclasses import dataclass
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.exception import CustomException
from src.logger import logging
from src.utils import save_file, save_object  # Tere utils se import kiya

@dataclass
class DataTransformationConfig:

    transformed_file_path: str = os.path.join('artifacts', "chunks.txt")

    transformed_obj_path: str = os.path.join('artifacts', "chunks.pkl")

class DataTransformation:
    def __init__(self):
        self.transformation_config = DataTransformationConfig()
        

    def initiate_data_transformation(self, transcript_path):
        try:
            logging.info("Data Transformation started")
            
            with open(transcript_path, 'r', encoding='utf-8') as f:
                text = f.read()

            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, 
                chunk_overlap=200
            )

            chunks = text_splitter.split_text(text)
            logging.info(f"Total chunks created: {len(chunks)}")

            
            formatted_text = ""
            for i, chunk in enumerate(chunks):
                formatted_text += f"--- Chunk {i+1} ---\n{chunk}\n\n"
            
            save_file(
                file_path=self.transformation_config.transformed_file_path,
                content=formatted_text
            )

            
            save_object(
                file_path=self.transformation_config.transformed_obj_path,
                obj=chunks
            )

            logging.info("Chunks and Objects saved via Utils successfully")
            return self.transformation_config.transformed_obj_path

        except Exception as e:
            raise CustomException(e, sys)


