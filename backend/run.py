import argparse
import sys
import uvicorn
from config import settings

def main():
    parser = argparse.ArgumentParser(description="Enterprise AI Assistant API")
    parser.add_argument(
        "--llm",
        type=str,
        choices=["openai", "groq", "gemini", "ollama"],
        default=settings.default_llm,
        help="LLM provider to use (default: openai)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Specific model name (optional, uses provider default if not specified)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development"
    )
    
    args = parser.parse_args()
    
    settings.default_llm = args.llm

    from main import app, current_llm_provider
    import main as main_module
    main_module.current_llm_provider = args.llm
    
    print(f"""
╔════════════════════════════════════════════════════════════╗
║         Enterprise AI Assistant - Starting Up              ║
╠════════════════════════════════════════════════════════════╣
║  LLM Provider: {args.llm.upper():<42}                      ║
║  Host:         {args.host:<42}                             ║
║  Port:         {args.port:<42}                             ║
║  Auto-reload:  {str(args.reload):<42}                      ║
╚════════════════════════════════════════════════════════════╝
""")
    
    try:
        uvicorn.run(
            "main:app",
            host=args.host,
            port=args.port,
            reload=args.reload
        )
    except KeyboardInterrupt:
        print("\n\nShutting down gracefully...")
        sys.exit(0)

if __name__ == "__main__":
    main()
