"""
Testes para validadores.
"""
import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.validators import CVValidator, DataValidator
from exceptions.custom_exceptions import InvalidCVLevelError

class TestCVValidator:
    """Testes para CVValidator."""
    
    def test_validate_cv_level_valid(self):
        """Testa validação de níveis válidos."""
        assert CVValidator.validate_cv_level(1) == 1
        assert CVValidator.validate_cv_level("15") == 15
        assert CVValidator.validate_cv_level(16) == 16
    
    def test_validate_cv_level_invalid(self):
        """Testa validação de níveis inválidos."""
        with pytest.raises(InvalidCVLevelError):
            CVValidator.validate_cv_level(0)
        
        with pytest.raises(InvalidCVLevelError):
            CVValidator.validate_cv_level(17)
        
        with pytest.raises(InvalidCVLevelError):
            CVValidator.validate_cv_level("abc")
    
    def test_extract_cv_from_message(self):
        """Testa extração de CV da mensagem."""
        assert CVValidator.extract_cv_from_message("Qual o melhor para CV 10?") == 10
        assert CVValidator.extract_cv_from_message("centro de vila 5") == 5
        assert CVValidator.extract_cv_from_message("TH 12 strategy") == 12
        assert CVValidator.extract_cv_from_message("Nada sobre CV aqui") is None

class TestDataValidator:
    """Testes para DataValidator."""
    
    def test_validate_required_fields(self):
        """Testa validação de campos obrigatórios."""
        data = {"name": "test", "level": 5}
        required = ["name", "level"]
        assert DataValidator.validate_required_fields(data, required) is True
        
        missing_required = ["name", "level", "missing"]
        assert DataValidator.validate_required_fields(data, missing_required) is False
    
    def test_sanitize_string(self):
        """Testa sanitização de strings."""
        assert DataValidator.sanitize_string("  test  ") == "test"
        assert DataValidator.sanitize_string("test\x00string") == "teststring"
        assert DataValidator.sanitize_string(123) == "123"
