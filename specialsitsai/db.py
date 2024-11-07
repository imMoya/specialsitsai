import os
from typing import List, Dict, Union, Optional
import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import re
import warnings
import structlog

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
logger = structlog.get_logger(__name__) 

class HTMLHandler:
    def __init__(self, save_directory: Optional[str] = None):
        if save_directory:
            self.save_directory = save_directory
            if not os.path.exists(self.save_directory):
                os.makedirs(self.save_directory)  

    @property
    def html_files(self) -> List[str]:
        """List all HTML files in the directory."""
        html_files = [
            file for file in os.listdir(self.save_directory)
            if file.endswith('.html') or file.endswith('.htm')
        ]
        return html_files
    
    @staticmethod
    def parse_html(filepath: str) -> str:
        """Parse HTML file to extract text content."""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
                text = soup.get_text(separator="\n")
                cleaned_text = re.sub(r'\s+', ' ', text)  # Normalize white spaces
                return cleaned_text.strip()
        except IOError as e:
            print(f"Error reading HTML file {filepath}: {e}")
            return ""

    @staticmethod
    def structure_text(text: str) -> Dict[str, str]:
        """Convert extracted text to a structured format."""
        structured_data = {
            "content": text
        }
        return structured_data

    @staticmethod
    def chunk_text(text: str, max_tokens: int = 512) -> List[str]:
        """Chunk text into smaller pieces for LLM processing."""
        words = text.split()
        chunks = [' '.join(words[i:i + max_tokens]) for i in range(0, len(words), max_tokens)]
        return chunks

    def process_html_files(self) -> List[Dict[str, Union[str, List[str]]]]:
        """Process all HTML files in the save directory and prepare them for LLM input."""
        processed_files = []
        for filename in os.listdir(self.save_directory):
            if filename.endswith('.htm') or filename.endswith('.html'):
                text = self.parse_html(os.path.join(self.save_directory, filename))
                processed_files.append({
                    "source": filename,
                    "page_content": text,
                })
        return processed_files
