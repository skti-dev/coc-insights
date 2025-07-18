"""
Constantes da aplicação.
"""

# Chaves de dados
class DataKeys:
    """Chaves usadas nos dados extraídos."""
    TOWN_HALL_LEVEL_REQUIRED = "Town Hall Level Required"
    LABORATORY_LEVEL_REQUIRED = "Laboratory Level Required"
    BARRACKS_LEVEL_REQUIRED = "Barracks Level Required"
    SPELL_FACTORY_LEVEL_REQUIRED = "Spell Factory Level Required"
    DARK_SPELL_FACTORY_LEVEL_REQUIRED = "Dark Spell Factory Level Required"
    PET_HOUSE_LEVEL_REQUIRED = "Pet House Level Required"
    WORKSHOP_LEVEL_REQUIRED = "Workshop Level Required"
    HERO_HALL_LEVEL_REQUIRED = "Hero Hall Level Required"
    TROOP_CAPACITY = "Troop Capacity"
    SPELL_STORAGE_CAPACITY = "Spell Storage Capacity"
    SIEGE_MACHINE_CAPACITY = "Siege Machine Capacity"

# Categorias
class Categories:
    """Categorias de dados do jogo."""
    SPELLS = "feitiços"
    HEROES = "heróis"
    PETS = "pets"
    TROOPS = "tropas"
    DEFENSES = "defesas"

# Arquivos de dados
class DataFiles:
    """Nomes dos arquivos de dados."""
    ARMY_DATABASE = "army_database.json"
    ARMY_BUILDINGS_DATABASE = "army_buildings_database.json"
    DEFENSES_DATABASE = "defenses_database.json"
    CV_CACHE = "cv_data_cache.json"
    SUMMARY_CACHE = "summary_cache.json"

# URLs
class URLs:
    """URLs utilizadas no web scraping."""
    CLASH_WIKI_BASE = "https://clashofclans.fandom.com/wiki/"
    SUPERCELL_NEWS = "https://supercell.com/en/games/clashofclans/pt/blog/"
    
# Limites
class Limits:
    """Limites da aplicação."""
    MAX_IMAGE_SIZE = 512
    MAX_TOKENS_VISION = 512
    MAX_UPLOAD_SIZE_MB = 2
