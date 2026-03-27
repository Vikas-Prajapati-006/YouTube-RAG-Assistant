import streamlit as st
import os
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.vector_store import VectorStore  # Added this
from src.pipeline.prediction_pipeline import RAGPipeline 


st.set_page_config(page_title="YouTube RAG Assistant", layout="wide")
st.title("YouTube Transcript Chatbot 🤖")


if "processed" not in st.session_state:
    st.session_state.processed = False
if "rag_obj" not in st.session_state:
    st.session_state.rag_obj = None


with st.sidebar:
    st.header("1. Data Setup")
    yt_url = st.text_input("Enter YouTube URL:")
    
    if st.button("Process & Initialize"):
        if yt_url:
            with st.spinner("Running the pipeline..."):
                try:
                    
                    ingestion = DataIngestion()
                    transcript_path = ingestion.initiate_data_ingestion(yt_url)
                    
                    
                    transformation = DataTransformation()
                   
                    chunks_obj_path = transformation.initiate_data_transformation(transcript_path)
                    
                    
                    vector_store_processor = VectorStore()
                    vector_store_processor.initiate_vector_store(chunks_obj_path)
                    
                    
                    st.session_state.rag_obj = RAGPipeline()
                    st.session_state.processed = True
                    
                    st.success("✅ System is ready! You can now ask questions.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a URL first!")


st.subheader("2. Ask Anything")

if st.session_state.processed:
    user_query = st.chat_input("Ask something about the video...")
    
    if user_query:
        with st.chat_message("user"):
            st.write(user_query)
            
        with st.chat_message("assistant"):
            with st.spinner("Generating answer..."):
                try:
                    
                    response = st.session_state.rag_obj.get_response(user_query)
                    st.write(response)
                except Exception as e:
                    st.error(f"Response error: {str(e)}")
else:
    st.info("👈 Please process a video from the sidebar to get started!")