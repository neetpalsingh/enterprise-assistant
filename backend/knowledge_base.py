from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from database.models import Document, get_db
from pathlib import Path
from datetime import datetime, timezone
import shutil
import uuid
import logging
import asyncio

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/knowledge", tags=["Knowledge Base"])

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_TYPES = ["policy", "compliance", "basic", "finance", "contract", "hr", "technical"]

_document_processor = None
_vector_store = None

def get_document_processor():
    global _document_processor
    if _document_processor is None:
        from rag.document_processor import DocumentProcessor
        _document_processor = DocumentProcessor()
    return _document_processor

def get_vector_store_instance():
    global _vector_store
    if _vector_store is None:
        from rag.vector_store import VectorStore
        _vector_store = VectorStore()
    return _vector_store

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

def _process_document_task(document_id: int):
    from database.models import SessionLocal
    db = SessionLocal()

    try:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            logger.error(f"Document {document_id} not found")
            return

        doc.status = "processing"
        db.commit()

        try:
            document_processor = get_document_processor()
            result = document_processor.process_document(doc.file_path)
        except MemoryError as e:
            logger.error(f"Memory error processing document {document_id}: {e}")
            doc.status = "failed"
            doc.error_message = f"Memory Error: {str(e)}"
            db.commit()
            return
        except ValueError as e:
            logger.error(f"Validation error processing document {document_id}: {e}")
            doc.status = "failed"
            doc.error_message = str(e)
            db.commit()
            return
        except Exception as e:
            error_msg = str(e).lower()
            logger.error(f"Document processing error for {document_id}: {e}")

            if "bad_alloc" in error_msg or "memory" in error_msg:
                doc.status = "failed"
                doc.error_message = "Out of memory. Try a smaller file."
            else:
                doc.status = "failed"
                doc.error_message = f"Processing failed: {str(e)}"

            db.commit()
            return

        try:
            vector_store = get_vector_store_instance()
            vector_store.add_document(
                document_id=str(doc.id),
                chunks=result['chunks'],
                metadata=result['metadata'],
                document_type=doc.document_type
            )
        except ValueError as e:
            error_msg = str(e)
            logger.error(f"Vector store error for {document_id}: {e}")

            if "OPENAI_API_KEY" in error_msg:
                doc.status = "failed"
                doc.error_message = "OpenAI API key not configured"
            else:
                doc.status = "failed"
                doc.error_message = str(e)

            db.commit()
            return
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Vector store error for {document_id}: {e}")

            if "api_key" in error_msg.lower() or "openai" in error_msg.lower():
                doc.status = "failed"
                doc.error_message = "OpenAI API key not configured. Check .env file and restart backend."
            else:
                doc.status = "failed"
                doc.error_message = f"Vector store failed: {str(e)}"

            db.commit()
            return

        doc.processed = True
        doc.status = "processed"
        doc.num_chunks = len(result['chunks'])
        doc.processed_at = datetime.now(timezone.utc)

        db.commit()
        logger.info(f"Document {document_id} processed successfully")

    except Exception as e:
        logger.error(f"Unexpected error processing document {document_id}: {e}")
        if doc:
            doc.status = "failed"
            doc.error_message = str(e)
            db.commit()
    finally:
        db.close()

@router.post("/process/{document_id}")
async def process_document(document_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(404, "Document not found")

    if doc.processed:
        raise HTTPException(400, "Document already processed")

    if doc.status == "processing":
        raise HTTPException(400, "Document is already being processed")

    doc.status = "processing"
    db.commit()

    background_tasks.add_task(_process_document_task, document_id)

    return {
        "id": doc.id,
        "file_name": doc.original_name,
        "status": "processing",
        "message": "Document processing started in background. Check status endpoint for progress."
    }

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
                "error_message": doc.error_message,
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
            vector_store = get_vector_store_instance()
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
