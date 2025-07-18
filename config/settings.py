"""
Configurações centralizadas da aplicação.
"""
import os
from pathlib import Path
from typing import Optional

class Settings:
    """Classe de configurações da aplicação."""
    
    # Diretórios
    ROOT_DIR = Path(__file__).parent.parent
    DATA_DIR = ROOT_DIR / "data"
    DB_DIR = ROOT_DIR / "db"
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Modelos
    MAIN_MODEL = "gpt-4o-mini"
    VISION_MODEL = "gpt-4o"
    TEMPERATURE = 0
    
    # Streamlit
    MAX_UPLOAD_SIZE: int = int(os.getenv("STREAMLIT_SERVER_MAX_UPLOAD_SIZE", "2"))
    
    # Banco de dados
    DATABASE_URL = f"sqlite:///{DB_DIR}/chat_history.db"
    
    # Cache
    CV_CACHE_FILE = DATA_DIR / "cv_data_cache.json"
    SUMMARY_CACHE_FILE = DATA_DIR / "summary_cache.json"
    
    # LangSmith (opcional)
    LANGSMITH_TRACING: Optional[str] = os.getenv("LANGSMITH_TRACING")
    LANGSMITH_ENDPOINT: Optional[str] = os.getenv("LANGSMITH_ENDPOINT")
    LANGSMITH_API_KEY: Optional[str] = os.getenv("LANGSMITH_API_KEY")
    LANGSMITH_PROJECT: Optional[str] = os.getenv("LANGSMITH_PROJECT")
    
    @classmethod
    def validate(cls) -> bool:
        """Valida se as configurações obrigatórias estão definidas."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY é obrigatória")
        return True

settings = Settings()
