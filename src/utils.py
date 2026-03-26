import os
import sys
import pickle
from src.exception import CustomException
from langchain_community.vectorstores import FAISS


def save_file(file_path, content):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    except Exception as e:
        raise CustomException(e, sys)


def save_object(file_path, obj):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as f:
            pickle.dump(obj, f)

    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_path):
    try:
        with open(file_path, "rb") as f:
            return pickle.load(f)
            
    except Exception as e:
        raise CustomException(e, sys)



def save_vector_store(folder_path, vector_store_obj):
    try:
        os.makedirs(os.path.dirname(folder_path), exist_ok=True)
        vector_store_obj.save_local(folder_path)
    except Exception as e:
        raise CustomException(e, sys)



def load_vector_store(folder_path, embeddings):
    try:
        if os.path.exists(folder_path):
            return FAISS.load_local(
                folder_path, 
                embeddings, 
                allow_dangerous_deserialization=True
            )
        else:
            raise Exception(f"Folder {folder_path} nahi mila bhai!")
    except Exception as e:
        raise CustomException(e, sys)