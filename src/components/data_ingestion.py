import os
import sys
import yt_dlp
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging

@dataclass
class DataIngestionConfig:
    # Final transcript file path
    raw_data_path: str = os.path.join('artifacts', "transcript.txt")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self, youtube_url):
        
        logging.info("Starting Data Ingestion: Fetching YouTube Transcript via yt-dlp")
        try:
           
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)

            
            ydl_opts = {
                'skip_download': True,         
                'writeautomaticsub': True,     
                'subtitleslangs': ['hi', 'en'],
                'outtmpl': os.path.join('artifacts', 'temp_subs'), 
                'quiet': True,
                'no_warnings': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                logging.info(f"Downloading transcript for URL: {youtube_url}")
                try:
                    ydl.download([youtube_url])
                except Exception as e:
                    
                    logging.warning(f"Partial error or 429 detected, checking for partial downloads: {str(e)}")

           
            artifacts_path = 'artifacts'
            temp_file = None
            
           
            all_files = os.listdir(artifacts_path)
            
            
            priority_extensions = ['.hi.vtt', '.en.vtt', '.vtt', '.srt']
            
            for ext in priority_extensions:
                for f in all_files:
                    if f.startswith('temp_subs') and f.endswith(ext):
                        temp_file = os.path.join(artifacts_path, f)
                        break
                if temp_file:
                    break

            if not temp_file:
                raise Exception("Error: Subtitle file not found. Please check the Video's CC (Closed Captions).")

            logging.info(f"Subtitle file found: {temp_file}. Converting to transcript.txt")

            
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()

            with open(self.ingestion_config.raw_data_path, 'w', encoding='utf-8') as f:
                f.write(content)

            
            for f in os.listdir(artifacts_path):
                if f.startswith('temp_subs'):
                    os.remove(os.path.join(artifacts_path, f))

            logging.info(f"Ingestion successful! Transcript saved: {self.ingestion_config.raw_data_path}")
            return self.ingestion_config.raw_data_path

        except Exception as e:
            raise CustomException(e, sys)