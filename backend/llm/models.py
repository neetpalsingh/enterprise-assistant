from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_models import ChatOllama
from langchain.chat_models.base import BaseChatModel
from config import settings

class LLMFactory:
    @staticmethod
    def create_llm(provider: str = "openai", model_name: Optional[str] = None, temperature: float = 0.7) -> BaseChatModel:
        provider = provider.lower()
        
        if provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OpenAI API key not configured")
            return ChatOpenAI(
                api_key=settings.openai_api_key,
                model=model_name or "gpt-4o-mini",
                temperature=temperature
            )
        
        elif provider == "groq":
            if not settings.groq_api_key:
                raise ValueError("Groq API key not configured")
            return ChatGroq(
                api_key=settings.groq_api_key,
                model=model_name or "llama-3.3-70b-versatile",
                temperature=temperature
            )
        
        elif provider == "gemini":
            if not settings.google_api_key:
                raise ValueError("Google API key not configured")
            return ChatGoogleGenerativeAI(
                google_api_key=settings.google_api_key,
                model=model_name or "gemini-1.5-flash",
                temperature=temperature
            )
        
        elif provider == "ollama":
            return ChatOllama(
                base_url=settings.ollama_base_url,
                model=model_name or "llama3.2",
                temperature=temperature
            )
        
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}. Supported: openai, groq, gemini, ollama")
    
    @staticmethod
    def get_available_providers() -> dict:
        return {
            "openai": bool(settings.openai_api_key),
            "groq": bool(settings.groq_api_key),
            "gemini": bool(settings.google_api_key),
            "ollama": True
        }
