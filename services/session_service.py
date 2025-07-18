"""
Serviços para gerenciamento de sessão e histórico.
"""
from typing import List
from utils.logger import get_logger
from models.domain import ChatMessage
from utils.db import load_history_from_db, clear_db_history as clear_db
from exceptions.custom_exceptions import DatabaseError

logger = get_logger(__name__)

class SessionService:
    """Serviço para gerenciamento de sessões."""
    
    @staticmethod
    def get_or_create_session_id(session_state) -> str:
        """Obtém ou cria um session_id."""
        if "session_id" not in session_state:
            session_state.session_id = 'Anônimo'
        return session_state.session_id
    
    @staticmethod
    def update_session_id(session_state, new_id: str) -> bool:
        """Atualiza o session_id se necessário."""
        if new_id != session_state.session_id:
            session_state.session_id = new_id
            return True
        return False

class HistoryService:
    """Serviço para gerenciamento de histórico."""
    
    @staticmethod
    def load_history(session_id: str) -> List[ChatMessage]:
        """Carrega o histórico da sessão."""
        try:
            return load_history_from_db(session_id)
        except Exception as e:
            logger.error(f"Erro ao carregar histórico: {e}")
            raise DatabaseError(f"Falha ao carregar histórico: {e}")
    
    @staticmethod
    def clear_history(session_id: str) -> None:
        """Limpa o histórico da sessão."""
        try:
            clear_db(session_id)
            logger.info(f"Histórico limpo para sessão: {session_id}")
        except Exception as e:
            logger.error(f"Erro ao limpar histórico: {e}")
            raise DatabaseError(f"Falha ao limpar histórico: {e}")
    
    @staticmethod
    def format_history_title(history: List[ChatMessage]) -> str:
        """Formata o título do histórico."""
        if not history:
            return ""
            
        first_message = history[0]['user']
        if len(first_message) > 50:
            return f"• Título: {first_message[:50]}..."
        return f"• Título: {first_message}"
