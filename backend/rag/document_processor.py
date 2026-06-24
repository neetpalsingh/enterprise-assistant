from docling.document_converter import DocumentConverter
from pathlib import Path
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self):
        self.converter = DocumentConverter()
    
    def process_document(self, file_path: str) -> Dict:
        try:
            result = self.converter.convert(file_path)
            
            text_content = result.document.export_to_markdown()
            
            chunks = self._create_chunks(text_content)
            
            return {
                "text": text_content,
                "chunks": chunks,
                "metadata": {
                    "file_name": Path(file_path).name,
                    "file_path": file_path,
                    "num_chunks": len(chunks)
                }
            }
        except Exception as e:
            logger.error(f"Error processing document {file_path}: {e}")
            raise
    
    def _create_chunks(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            
            if end < text_length:
                last_period = text.rfind('.', start, end)
                last_newline = text.rfind('\n', start, end)
                split_point = max(last_period, last_newline)
                
                if split_point > start:
                    end = split_point + 1
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap if end < text_length else text_length
        
        return chunks
    
    def validate_file(self, file_path: str) -> bool:
        valid_extensions = ['.pdf', '.docx', '.doc']
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext not in valid_extensions:
            raise ValueError(f"Unsupported file format: {file_ext}. Supported: {valid_extensions}")
        
        if not Path(file_path).exists():
            raise ValueError(f"File not found: {file_path}")
        
        return True
