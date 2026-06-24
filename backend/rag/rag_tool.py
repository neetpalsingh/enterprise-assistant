from typing import Dict, Optional
from langchain_core.tools import tool
import logging
import re

logger = logging.getLogger(__name__)

_vector_store = None

def get_vector_store():
    global _vector_store
    if _vector_store is None:
        from .vector_store import VectorStore
        _vector_store = VectorStore()
    return _vector_store

def needs_knowledge_base(question: str) -> bool:
    knowledge_keywords = [
        'policy', 'policies', 'compliance', 'procedure', 'guideline',
        'document', 'handbook', 'manual', 'regulation', 'rule',
        'contract', 'agreement', 'finance', 'financial', 'budget',
        'according to', 'based on document', 'what does the', 'refer to',
        'documentation', 'standard', 'protocol'
    ]
    
    question_lower = question.lower()
    return any(keyword in question_lower for keyword in knowledge_keywords)

def detect_document_type(question: str) -> Optional[str]:
    question_lower = question.lower()
    
    if any(word in question_lower for word in ['policy', 'policies']):
        return 'policy'
    elif any(word in question_lower for word in ['compliance', 'compliant', 'regulation']):
        return 'compliance'
    elif any(word in question_lower for word in ['finance', 'financial', 'budget', 'expense']):
        return 'finance'
    elif any(word in question_lower for word in ['contract', 'agreement']):
        return 'contract'
    
    return None

@tool
def search_knowledge_base(question: str) -> str:
    """
    Search the knowledge base for relevant information from uploaded documents.
    Use this when the question is about policies, compliance, procedures, or any documented information.

    Args:
        question: The user's question

    Returns:
        Relevant information from documents with source citations
    """
    try:
        if not needs_knowledge_base(question):
            return "This question doesn't require knowledge base search."

        document_type = detect_document_type(question)

        vector_store = get_vector_store()
        results = vector_store.query(
            query_text=question,
            document_type=document_type,
            n_results=5
        )
        
        if not results['documents']:
            return "No relevant information found in the knowledge base."
        
        response_parts = []
        response_parts.append("Based on the knowledge base:\n")
        
        for i, (doc, source) in enumerate(zip(results['documents'], results['sources']), 1):
            response_parts.append(f"\n**Source {i}: {source['file_name']}** (Type: {source['document_type']})")
            response_parts.append(f"{doc}\n")
        
        sources_list = list(set([s['file_name'] for s in results['sources']]))
        response_parts.append(f"\n---\nSources: {', '.join(sources_list)}")
        
        return "\n".join(response_parts)
        
    except Exception as e:
        logger.error(f"Error in knowledge base search: {e}")
        return f"Error searching knowledge base: {str(e)}"

def get_rag_tool():
    return search_knowledge_base
