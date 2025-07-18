"""
Sistema de logging configurado para a aplicação.
"""
import logging
import sys
from pathlib import Path
from typing import Optional

class LoggerSetup:
    """Configuração do sistema de logging."""
    
    @staticmethod
    def setup_logger(
        name: str,
        level: int = logging.INFO,
        log_file: Optional[Path] = None
    ) -> logging.Logger:
        """
        Configura e retorna um logger.
        
        Args:
            name: Nome do logger
            level: Nível de logging
            log_file: Arquivo de log (opcional)
            
        Returns:
            Logger configurado
        """
        logger = logging.getLogger(name)
        
        # Evita duplicação de handlers
        if logger.handlers:
            return logger
            
        logger.setLevel(level)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler (se especificado)
        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger

def get_logger(name: str) -> logging.Logger:
    """Retorna um logger configurado para o módulo."""
    return LoggerSetup.setup_logger(name)
