import os
import sys
from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEmbeddings, ChatHuggingFace
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from src.exception import CustomException
from src.logger import logging
from src.utils import load_vector_store
from dotenv import load_dotenv

load_dotenv()

class RAGPipeline:
    def __init__(self):
        try:
            logging.info("Initializing RAG Pipeline with ChatHuggingFace...")
            
           
            self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            
            
            self.vector_db_path = os.path.join("artifacts", "faiss_index")
            self.vector_db = load_vector_store(
                folder_path=self.vector_db_path, 
                embeddings=self.embeddings
            )
            
            
            llm = HuggingFaceEndpoint(
                repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
                huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
                temperature=0.7,
                max_new_tokens=512,
            )
            
            
            self.chat_model = ChatHuggingFace(llm=llm)
            
            logging.info("RAG Pipeline initialized with Chat Wrapper!")

        except Exception as e:
            raise CustomException(e, sys)

    def get_response(self, query):
        try:
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", "Answer the question based on the provided context. Context: {context}"),
                ("human", "{question}")
            ])

            
            retriever = self.vector_db.as_retriever(search_kwargs={"k": 3})

            
            rag_chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | prompt
                | self.chat_model
                | StrOutputParser()
            )

            logging.info(f"Querying: {query}")
            return rag_chain.invoke(query)

        except Exception as e:
            raise CustomException(e, sys)