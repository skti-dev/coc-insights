"""
Exceções personalizadas para a aplicação.
"""

class COCInsightsError(Exception):
    """Exceção base da aplicação."""
    pass

class DatabaseError(COCInsightsError):
    """Erro relacionado ao banco de dados."""
    pass

class ConfigurationError(COCInsightsError):
    """Erro de configuração."""
    pass

class WebScrapingError(COCInsightsError):
    """Erro no web scraping."""
    pass

class ImageProcessingError(COCInsightsError):
    """Erro no processamento de imagem."""
    pass

class CVDataNotFoundError(COCInsightsError):
    """Dados do CV não encontrados."""
    pass

class InvalidCVLevelError(COCInsightsError):
    """Nível de CV inválido."""
    pass
