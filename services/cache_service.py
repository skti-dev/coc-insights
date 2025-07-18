"""
Sistema de cache melhorado com interface abstrata.
"""
import json
import hashlib
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional
from utils.logger import get_logger
from exceptions.custom_exceptions import COCInsightsError

logger = get_logger(__name__)

class CacheInterface(ABC):
    """Interface para sistemas de cache."""
    
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Obtém um valor do cache."""
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Define um valor no cache."""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Limpa o cache."""
        pass

class JSONFileCache(CacheInterface):
    """Cache baseado em arquivo JSON."""
    
    def __init__(self, cache_file: Path):
        self.cache_file = Path(cache_file)
        self._cache: Dict[str, Any] = {}
        self._load_cache()
    
    def _load_cache(self) -> None:
        """Carrega o cache do arquivo."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self._cache = json.load(f)
                logger.info(f"Cache carregado de {self.cache_file}")
            except Exception as e:
                logger.error(f"Erro ao carregar cache: {e}")
                self._cache = {}
        else:
            self._cache = {}
    
    def _save_cache(self) -> None:
        """Salva o cache no arquivo."""
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self._cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Erro ao salvar cache: {e}")
            raise COCInsightsError(f"Falha ao salvar cache: {e}")
    
    def get(self, key: str) -> Optional[Any]:
        """Obtém um valor do cache."""
        return self._cache.get(key)
    
    def set(self, key: str, value: Any) -> None:
        """Define um valor no cache."""
        self._cache[key] = value
        self._save_cache()
    
    def clear(self) -> None:
        """Limpa o cache."""
        self._cache.clear()
        self._save_cache()
    
    def hash_key(self, data: Any) -> str:
        """Gera hash para usar como chave."""
        if isinstance(data, dict):
            data_str = json.dumps(data, sort_keys=True)
        elif isinstance(data, list):
            data_str = '\n'.join(sorted(str(item) for item in data))
        else:
            data_str = str(data)
        
        return hashlib.md5(data_str.encode('utf-8')).hexdigest()

class CacheManager:
    """Gerenciador de múltiplos caches."""
    
    def __init__(self):
        self._caches: Dict[str, CacheInterface] = {}
    
    def register_cache(self, name: str, cache: CacheInterface) -> None:
        """Registra um cache."""
        self._caches[name] = cache
    
    def get_cache(self, name: str) -> Optional[CacheInterface]:
        """Obtém um cache pelo nome."""
        return self._caches.get(name)
