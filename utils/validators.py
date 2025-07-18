"""
Validadores para dados da aplicação.
"""
import re
from typing import Optional, Union
from utils.logger import get_logger
from exceptions.custom_exceptions import InvalidCVLevelError

logger = get_logger(__name__)

class CVValidator:
    """Validador para dados de Centro de Vila."""
    
    @staticmethod
    def validate_cv_level(cv_level: Union[str, int]) -> int:
        """
        Valida se o nível do CV está dentro do range válido.
        
        Args:
            cv_level: Nível do CV
            
        Returns:
            Nível do CV validado
            
        Raises:
            InvalidCVLevelError: Se o nível for inválido
        """
        try:
            level = int(cv_level)
            if not (1 <= level <= 16):  # Range atual do jogo
                raise InvalidCVLevelError(f"Nível de CV deve estar entre 1 e 16, recebido: {level}")
            return level
        except ValueError:
            raise InvalidCVLevelError(f"Nível de CV inválido: {cv_level}")
    
    @staticmethod
    def extract_cv_from_message(message: str) -> Optional[int]:
        """
        Extrai o nível do CV de uma mensagem.
        
        Args:
            message: Mensagem do usuário
            
        Returns:
            Nível do CV ou None se não encontrado
        """
        # Padrões para identificar CV na mensagem
        patterns = [
            r'cv\s*(\d+)',
            r'centro\s+de\s+vila\s+(\d+)',
            r'town\s+hall\s+(\d+)',
            r'th\s*(\d+)',
            r'level\s+(\d+)',
            r'nível\s+(\d+)'
        ]
        
        message_lower = message.lower()
        
        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                try:
                    level = int(match.group(1))
                    return CVValidator.validate_cv_level(level)
                except InvalidCVLevelError:
                    continue
        
        return None

class DataValidator:
    """Validador geral para dados."""
    
    @staticmethod
    def validate_required_fields(data: dict, required_fields: list) -> bool:
        """
        Valida se todos os campos obrigatórios estão presentes.
        
        Args:
            data: Dicionário de dados
            required_fields: Lista de campos obrigatórios
            
        Returns:
            True se todos os campos estão presentes
        """
        missing_fields = [field for field in required_fields if field not in data or data[field] is None]
        
        if missing_fields:
            logger.warning(f"Campos obrigatórios ausentes: {missing_fields}")
            return False
        
        return True
    
    @staticmethod
    def sanitize_string(text: str) -> str:
        """
        Sanitiza uma string removendo caracteres perigosos.
        
        Args:
            text: Texto a ser sanitizado
            
        Returns:
            Texto sanitizado
        """
        if not isinstance(text, str):
            return str(text)
        
        # Remove caracteres de controle
        sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        
        # Remove excesso de espaços
        sanitized = ' '.join(sanitized.split())
        
        return sanitized.strip()
