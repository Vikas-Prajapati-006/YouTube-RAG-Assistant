import os
import sys
from src.exception import CustomException
from src.logger import logging
from youtube_transcript_api import YouTubeTranscriptApi



from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    
    raw_data_path: str = os.path.join('artifacts', "transcript.txt")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        # Artifacts directory banana agar nahi hai toh
        os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)

    def extract_video_id(self, url):

        try:
            logging.info(f"Extracting Video ID from URL: {url}")
            if "v=" in url:
                return url.split("v=")[1].split("&")[0]
            elif "be/" in url:
                return url.split(".be/")[1].split("?")[0]
            return url
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_ingestion(self, video_url):
        logging.info("Entered the data ingestion method or component")
        try:
            video_id = self.extract_video_id(video_url)
            logging.info(f"Fetching transcript for Video ID: {video_id}")

            
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            
            try:
                transcript = transcript_list.find_transcript(['hi', 'en'])
            except:
               
                transcript = transcript_list.find_generated_transcript(['hi', 'en'])

            transcript_data = transcript.fetch()
            
            
            full_text = " ".join([t['text'] for t in transcript_data])

            
            with open(self.ingestion_config.raw_data_path, "w", encoding="utf-8") as f:
                f.write(full_text)

            logging.info("Ingestion of the data is completed successfully")
            return self.ingestion_config.raw_data_path

        except Exception as e:
            logging.error(f"Exception occurred at Data Ingestion stage: {str(e)}")
            raise CustomException(e, sys)
