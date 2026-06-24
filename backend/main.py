from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from schemas import AskRequest, AskResponse, ErrorResponse, HealthResponse
from agent.graph import EnterpriseAgent
from database.models import init_db
from database.seed import seed_demo_data
from llm.models import LLMFactory
from config import settings

try:
    from knowledge_base import router as knowledge_router
    KNOWLEDGE_BASE_AVAILABLE = True
except ImportError as e:
    logger = logging.getLogger(__name__)
    logger.warning(f"Knowledge base dependencies not installed: {e}")
    KNOWLEDGE_BASE_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

agent: EnterpriseAgent = None
current_llm_provider: str = settings.default_llm

@asynccontextmanager
async def lifespan(app: FastAPI):
    global agent
    logger.info("Initializing database...")
    init_db()
    seed_demo_data()
    
    logger.info(f"Initializing AI agent with {current_llm_provider} provider...")
    try:
        agent = EnterpriseAgent(llm_provider=current_llm_provider)
        logger.info("Agent initialized successfully!")
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}")
        raise
    
    yield
    
    logger.info("Shutting down...")

app = FastAPI(
    title="Enterprise AI Assistant",
    description="AI-powered assistant for business operations with conversation memory and tool calling",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if KNOWLEDGE_BASE_AVAILABLE:
    app.include_router(knowledge_router)
    logger.info("Knowledge base endpoints enabled")
else:
    logger.info("Knowledge base endpoints disabled (dependencies not installed)")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            detail=str(exc)
        ).model_dump()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc)
        ).model_dump()
    )

@app.get("/", response_model=dict)
async def root():
    return {
        "message": "Enterprise AI Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "POST /ask": "Ask a question to the AI assistant",
            "GET /health": "Check API health and configuration"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="healthy",
        llm_provider=current_llm_provider,
        available_providers=LLMFactory.get_available_providers()
    )

@app.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    try:
        if not agent:
            raise HTTPException(status_code=503, detail="Agent not initialized")

        logger.info(f"Processing question: {request.question[:100]}...")

        answer = agent.run(
            question=request.question,
            thread_id=request.thread_id
        )

        logger.info(f"Response generated successfully for thread: {request.thread_id}")

        return AskResponse(
            answer=answer,
            thread_id=request.thread_id,
            success=True
        )

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to process request: {str(e)}")

@app.get("/employees")
async def get_employees():
    from database.models import SessionLocal, Employee
    db = SessionLocal()
    try:
        employees = db.query(Employee).all()
        return [
            {
                "id": emp.id,
                "name": emp.name,
                "email": emp.email,
                "position": emp.position,
                "department": emp.department,
                "salary": emp.salary
            }
            for emp in employees
        ]
    finally:
        db.close()

@app.get("/tickets")
async def get_tickets():
    from database.models import SessionLocal, Ticket
    db = SessionLocal()
    try:
        tickets = db.query(Ticket).all()
        return [
            {
                "id": tick.id,
                "title": tick.title,
                "description": tick.description,
                "status": tick.status,
                "priority": tick.priority,
                "assigned_to": tick.assigned_to,
                "created_at": tick.created_at.isoformat() if tick.created_at else None
            }
            for tick in tickets
        ]
    finally:
        db.close()

@app.get("/reports")
async def get_reports():
    from database.models import SessionLocal, Report
    db = SessionLocal()
    try:
        reports = db.query(Report).all()
        return [
            {
                "id": rep.id,
                "title": rep.title,
                "content": rep.content,
                "report_type": rep.report_type,
                "created_at": rep.created_at.isoformat() if rep.created_at else None
            }
            for rep in reports
        ]
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
