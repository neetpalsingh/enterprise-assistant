from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from database.models import Document, get_db
from rag.document_processor import DocumentProcessor
from rag.vector_store import VectorStore
from pathlib import Path
from datetime import datetime
import shutil
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/knowledge", tags=["Knowledge Base"])

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_TYPES = ["policy", "compliance", "basic", "finance", "contract", "hr", "technical"]

document_processor = DocumentProcessor()
vector_store = VectorStore()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        if document_type not in ALLOWED_TYPES:
            raise HTTPException(400, f"Invalid document type. Allowed: {ALLOWED_TYPES}")
        
        if not file.filename:
            raise HTTPException(400, "No file provided")
        
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ['.pdf', '.docx', '.doc']:
            raise HTTPException(400, f"Unsupported file type: {file_ext}")
        
        file_id = str(uuid.uuid4())
        file_name = f"{file_id}{file_ext}"
        file_path = UPLOAD_DIR / file_name
        
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_size = file_path.stat().st_size
        
        doc = Document(
            file_name=file_name,
            original_name=file.filename,
            file_path=str(file_path),
            file_size=file_size,
            document_type=document_type,
            status="uploaded",
            processed=False
        )
        
        db.add(doc)
        db.commit()
        db.refresh(doc)
        
        return {
            "id": doc.id,
            "file_name": doc.original_name,
            "document_type": doc.document_type,
            "status": doc.status,
            "size": doc.file_size,
            "message": "File uploaded successfully. Click 'Process' to add to knowledge base."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(500, f"Upload failed: {str(e)}")

@router.post("/process/{document_id}")
async def process_document(document_id: int, db: Session = Depends(get_db)):
    try:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            raise HTTPException(404, "Document not found")
        
        if doc.processed:
            raise HTTPException(400, "Document already processed")
        
        result = document_processor.process_document(doc.file_path)
        
        vector_store.add_document(
            document_id=str(doc.id),
            chunks=result['chunks'],
            metadata=result['metadata'],
            document_type=doc.document_type
        )
        
        doc.processed = True
        doc.status = "processed"
        doc.num_chunks = len(result['chunks'])
        doc.processed_at = datetime.utcnow()
        
        db.commit()
        db.refresh(doc)
        
        return {
            "id": doc.id,
            "file_name": doc.original_name,
            "status": doc.status,
            "chunks": doc.num_chunks,
            "message": "Document processed and added to knowledge base"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Processing error: {e}")
        raise HTTPException(500, f"Processing failed: {str(e)}")

@router.get("/documents")
async def list_documents(db: Session = Depends(get_db)):
    try:
        docs = db.query(Document).order_by(Document.uploaded_at.desc()).all()
        return [
            {
                "id": doc.id,
                "file_name": doc.original_name,
                "document_type": doc.document_type,
                "status": doc.status,
                "processed": doc.processed,
                "size": doc.file_size,
                "chunks": doc.num_chunks,
                "uploaded_at": doc.uploaded_at.isoformat(),
                "processed_at": doc.processed_at.isoformat() if doc.processed_at else None
            }
            for doc in docs
        ]
    except Exception as e:
        logger.error(f"List error: {e}")
        raise HTTPException(500, f"Failed to list documents: {str(e)}")

@router.delete("/documents/{document_id}")
async def delete_document(document_id: int, db: Session = Depends(get_db)):
    try:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            raise HTTPException(404, "Document not found")
        
        if doc.processed:
            vector_store.delete_document(str(doc.id))
        
        file_path = Path(doc.file_path)
        if file_path.exists():
            file_path.unlink()
        
        db.delete(doc)
        db.commit()
        
        return {"message": "Document deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete error: {e}")
        raise HTTPException(500, f"Delete failed: {str(e)}")
