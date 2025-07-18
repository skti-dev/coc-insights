"""
Modelos de dados e DTOs para o domínio do Clash of Clans.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum

class MessageCategory(Enum):
    """Categorias de mensagens do usuário."""
    ATTACK_STRATEGY = "estrategia de ataque"
    CV_INFO = "informacoes do CV"
    UPDATE = "atualizacoes"
    OTHERS = "outros"

@dataclass
class TroopLevel:
    """Representa um nível de tropa."""
    level: str
    hitpoints: Optional[str] = None
    damage_per_second: Optional[str] = None
    town_hall_required: Optional[str] = None
    cost: Optional[str] = None
    
@dataclass
class DefenseInfo:
    """Informações de uma defesa."""
    name_pt: str
    name_en: str
    level: str
    damage_per_second: str
    hitpoints: str
    offensive_strategies: str

@dataclass
class CVData:
    """Dados de um Centro de Vila específico."""
    cv_level: int
    tropas: Dict[str, Any]
    feiticos: Dict[str, Any]
    herois: Dict[str, Any]
    pets: Dict[str, Any]
    estruturas: Dict[str, Any]

@dataclass
class ImageAnalysis:
    """Resultado da análise de imagem."""
    cv_level: str
    defenses: List[Dict[str, str]]
    image_analysis: str

@dataclass
class ChatMessage:
    """Mensagem do chat."""
    user: str
    bot: str
    timestamp: Optional[str] = None

@dataclass
class UserInput:
    """Input do usuário."""
    message: str
    image_path: Optional[str] = None
    session_id: str = "Anônimo"
