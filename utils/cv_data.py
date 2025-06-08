from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import json
import hashlib
import sys
import os
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

CV_CACHE_FILE = 'data/cv_data_cache.json'
cv_data_cache = {}

THLR = "Town Hall Level Required"
LLR = "Laboratory Level Required"
BLR = "Barracks Level Required"
SFLR = "Spell Factory Level Required"
DFLR = "Dark Spell Factory Level Required"
PHLR = "Pet House Level Required"
WHLR = "Workshop Level Required"
HHLR = "Hero Hall Level Required"
TC = "Troop Capacity"
SSC = "Spell Storage Capacity"
SMC = "Siege Machine Capacity"
SPELLS = "feitiços"
HEROS = "heróis"

def load_cv_cache():
  global cv_data_cache
  if os.path.exists(CV_CACHE_FILE):
    try:
      with open(CV_CACHE_FILE, 'r', encoding='utf-8') as f:
        cv_data_cache = json.load(f)
    except Exception as e:
      print(f"Erro ao carregar cache: {e}")
      cv_data_cache = {}
  else:
    cv_data_cache = {}

def save_cv_cache():
  try:
    with open(CV_CACHE_FILE, 'w', encoding='utf-8') as f:
      json.dump(cv_data_cache, f, ensure_ascii=False, indent=2)
  except Exception as e:
    print(f"Erro ao salvar cache: {e}")
    
def hash_cv_data(cv_data: dict) -> str:
  joined = json.dumps(cv_data, sort_keys=True)
  return hashlib.md5(joined.encode('utf-8')).hexdigest()

def verify_if_user_mentioned_cv(user_message: str) -> str:
  cv_check_chat = ChatOpenAI(model='gpt-4o-mini', temperature=0)
  cv_check_prompt = ChatPromptTemplate.from_template(
    """
    Você é um especialista no jogo Clash of Clans e deve verificar se o usuário mencionou um Centro de Vila (CV) específico em sua mensagem.

    ### Instruções:
    Analise a mensagem do usuário e determine se ele mencionou um CV específico (por exemplo, "CV 10", "Centro de Vila 12", etc.).

    ### Regras:
    - Responda com o número do CV se um CV foi mencionado, ou "não" caso contrário.

    ### Mensagem do usuário:
    {user_message}
    """
  )
  cv_check_chain = cv_check_prompt | cv_check_chat
  
  response = cv_check_chain.invoke({"user_message": user_message}).content.strip().lower()
  return response

def parse_required(th_str):
  try:
    return int(''.join(filter(str.isdigit, th_str)))
  except ValueError:
    print(f"Erro ao analisar o nível do CV: {th_str}")
    return float('inf')
  
def filter_by_cv(levels, cv_level):
  return [
    lvl for lvl in levels
    if lvl.get(THLR) and parse_required(lvl[THLR]) <= cv_level
  ]

def parse_int(value):
  try:
    return int(''.join(filter(str.isdigit, value)))
  except ValueError:
    print(f"Erro ao analisar o valor: {value}")
    return float('inf')

def building_requires(building_key, required_level, buildings_data=None, cv_level=0):
  if not buildings_data or building_key not in buildings_data:
    return False
  for level in buildings_data[building_key]["levels"]:
    if level.get("Level") == str(required_level):
      th_required = level.get(THLR)
      return th_required and parse_int(th_required) <= cv_level
  return False

def get_max_level(levels, cv_level, buildings_data=None):
  valids = []
  for lvl in levels:
    if THLR in lvl and parse_int(lvl[THLR]) <= cv_level:
      valids.append(lvl)
    else:
      building_keys = {
        LLR: "laboratory",
        BLR: "barracks",
        SFLR: "spell_factory",
        DFLR: "dark_spell_factory",
        HHLR: "hero_hall",
        PHLR: "pet_house",
        WHLR: "workshop"
      }
      for req_key, building in building_keys.items():
        if req_key in lvl and building_requires(building, lvl[req_key], buildings_data, cv_level):
          valids.append(lvl)
          break

  return valids[-1] if valids else {}

def load_databases():
  try:
    with open("data/army_database.json", encoding='utf-8') as f:
      army_data = json.load(f)
    with open("data/army_buildings_database.json", encoding='utf-8') as f:
      buildings_data = json.load(f)
    return army_data, buildings_data
  except Exception as e:
    print(f"Erro ao carregar bases: {e}")
    return None, None

def proccess_army_data(army_data, buildings_data, cv_level):
  result = {
    "tropas": {},
    SPELLS: {},
    HEROS: {},
    "pets": {}
  }

  for nome, dados in army_data.items():
    nivel = get_max_level(dados.get("levels", []), cv_level, buildings_data)
    if not nivel:
      continue
    if SFLR in nivel or DFLR in nivel or ("Housing Space" in nivel and "tiles" in nivel["Housing Space"]):
      result[SPELLS][nome] = nivel
    elif HHLR in nivel or "Health Recovery" in nivel:
      result[HEROS][nome] = nivel
    elif PHLR in nivel:
      result["pets"][nome] = nivel
    else:
      result["tropas"][nome] = nivel

  return result

def proccess_buildings_data(buildings_data, cv_level):
  structures = {}
  for estrutura, dados in buildings_data.items():
    nivel = get_max_level(dados.get("levels", []), cv_level)
    if nivel:
      structures[estrutura] = {
        "Level": nivel.get("Level"),
        TC: nivel.get(TC),
        "Number of Buildings": dados.get("number_of_buildings", "1"),
        SSC: nivel.get(SSC, "0"),
        SMC: nivel.get(SMC, "0"),
        "Max Troops": int(nivel.get(TC, 0)) * int(dados.get("number_of_buildings", "1")),
        "Max Spells": int(nivel.get(SSC, 0)) * int(dados.get("number_of_buildings", "1")),
        "Max Siege Machines": int(nivel.get(SMC, 0)) * int(dados.get("number_of_buildings", "1")),
      }
      
  return structures

def extract_cv_number(text: str) -> int:
  match = re.search(r"\d+", text)
  return int(match.group()) if match else None

def get_cv_data(user_message: str) -> dict:
  cv_level = verify_if_user_mentioned_cv(user_message)
  if cv_level == "não":
    print(f"Nenhum CV mencionado na mensagem do usuário: {user_message}")
    return {}

  cv_level = extract_cv_number(cv_level)
  if not cv_level:
    print(f"CV não encontrado na mensagem do usuário: {user_message}")
    return {}
  
  if cv_level in cv_data_cache:
    print(f"Dados do CV {cv_level} encontrados no cache.")
    return cv_data_cache[cv_level]

  army_data, buildings_data = load_databases()
  if not army_data or not buildings_data:
    print("Erro ao carregar as bases de dados de tropas e construções.")
    return {}

  army_result = proccess_army_data(army_data, buildings_data, cv_level)
  estruturas_result = proccess_buildings_data(buildings_data, cv_level)

  result = {
    "cv_level": cv_level,
    "tropas": army_result["tropas"],
    SPELLS: army_result[SPELLS],
    HEROS: army_result[HEROS],
    "pets": army_result["pets"],
    "estruturas": estruturas_result
  }

  cv_data_cache[cv_level] = result
  save_cv_cache()
  return result

def test_get_cv_data():
  user_message = "Dados disponíveis para CV 9"
  cv_data = get_cv_data(user_message)
  print(json.dumps(cv_data, indent=2, ensure_ascii=False))

load_cv_cache()

if __name__ == "__main__":
  test_get_cv_data()
