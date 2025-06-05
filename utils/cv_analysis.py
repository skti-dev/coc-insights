from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from PIL import Image
from io import BytesIO
import base64
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def resize_image_to_base64(image_path: str, max_size: int = 512) -> str:
  with Image.open(image_path) as img:
    img.thumbnail((max_size, max_size))
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def image_analysis(image_path: str): 
  image_chat = ChatOpenAI(model="gpt-4o", max_tokens=512)
  image_b64 = resize_image_to_base64(image_path)

  response = image_chat.invoke([
    SystemMessage(content=(
      "Você é um especialista em Clash of Clans especializado em análise de imagens de vilas. "
      "Sua tarefa é analisar a imagem de uma vila e extrair informações exclusivamente sobre defesas, armadilhas visíveis e layout. "
      "Ignore completamente construções que não sejam defesas ou armadilhas (como armazéns, minas, quartéis, acampamentos, etc). "
      "Se possível, determine o nível do Centro de Vila (CV) com base nas defesas visíveis.\n\n"

      "### Instruções:\n"
      "- Identifique todas as defesas e armadilhas visíveis na imagem.\n"
      "- Liste cada defesa com seu nome e nível aproximado (se for possível identificar visualmente).\n"
      "- Inclua armadilhas (como bombas, armadilhas de mola, bombas aéreas, minas de busca, etc) caso estejam visíveis.\n"
      "- Se o nível do CV puder ser inferido com base nas defesas, informe-o no campo 'cv_level'. Caso contrário, use 'desconhecido'.\n"
      "- Caso a imagem não tenha qualidade suficiente ou não permita análise, responda com: 'Imagem insuficiente para análise'.\n\n"

      "### Formato da resposta:\n"
      "Responda em JSON com os seguintes campos:\n"
      "- 'cv_level': string (ex: '5', '10', '15', ou 'desconhecido')\n"
      "- 'defenses': lista de objetos com nome e nível aproximado, ex: [{\"nome\": \"Canhão\", \"nível\": \"6\"}]\n"
      "- 'image_analysis': breve descrição textual do layout da vila"
    )),
    HumanMessage(content=[
      {"type": "text", "text": "Analise esta vila:"},
      {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}}
    ])
  ])
  
  data = response.content.strip()
  try:
    cleaned_str = data.removeprefix("```json").removesuffix("```")
    data = json.loads(cleaned_str)
  except json.JSONDecodeError:
    raise ValueError("A resposta não está no formato JSON esperado. Verifique a análise da imagem.")
  
  return data

def map_portuguese_to_english(name_pt):
  mapping = {
    "Canhão": "Cannon",
    "Torre de Arqueiras": "Archer Tower",
    "Morteiro": "Mortar",
    "Antiaérea": "Air Defense",
    "Defesa Aérea": "Air Defense",
    "Torre do Mago": "Wizard Tower",
    "Torre de Magos": "Wizard Tower",
    "Torre de Besta": "X-Bow",
    "Torre Inferno": "Inferno Tower",
    "Torre de Bombardeio": "Bomb Tower",
    "Dispensador de Ar": "Air Sweeper",
    "Tesla Oculta": "Hidden Tesla",
    "Artilharia Águia": "Eagle Artillery",
    "Disseminador": "Scattershot",
    "Cabana do Construtor": "Builder's Hut",
    "Torre de Feitiços": "Spell Tower",
    "Monólito": "Monolith",
    "Torre Multi-Arqueira": "Multi-Archer Tower",
    "Canhão Ricochete": "Ricochet Cannon",
    "Torre Multi-Gear": "Multi-Gear Tower",
    "Fogo Fátuo": "Firespitter",
    "Muro": "Wall",
    "Centro de Vila": "Town Hall",
    "Giga Tesla": "Giga Tesla",
    "Giga Inferno": "Giga Inferno",
    "TH13": "TH13",
    "TH14": "TH14",
    "TH15": "TH15",
    "TH16": "TH16",
    "Artilharia Inferno": "Inferno Artillery",
    "Armadilhas": "Traps",
    "Bomba": "Bomb",
    "Armadilha de Mola": "Spring Trap",
    "Bomba Aérea": "Air Bomb",
    "Bomba Gigante": "Giant Bomb",
    "Mina Aérea Guiada": "Seeking Air Mine",
    "Armadilha de Esqueleto": "Skeleton Trap",
    "Armadilha Tornado": "Tornado Trap",
    "Bomba Giga": "Giga Bomb"
  }
  return mapping.get(name_pt, None)

def extract_defense_details(analysis, path_to_database):
  output = {}
  base_json = {}
  
  try:
    with open(path_to_database, 'r', encoding='utf-8') as file:
      base_json = json.load(file)
  except FileNotFoundError:
    raise FileNotFoundError(f"Arquivo de base de dados '{path_to_database}' não encontrado.")
  
  for defesa in analysis["defenses"]:
    nome_pt = defesa["nome"]
    nivel_str = defesa["nível"]
    nome_en = map_portuguese_to_english(nome_pt)

    if not nome_en or nome_en not in base_json:
      print(f"Defesa '{nome_pt}'('{nome_en}') não encontrada na base de dados ou não mapeada corretamente.")
      continue

    defesa_info = base_json[nome_en]
    level_data = next((lvl for lvl in defesa_info["levels"] if lvl["Level"] == nivel_str), None)

    if not level_data:
      print(f"Nível '{nivel_str}' para defesa '{nome_pt}' não encontrado na base de dados.")
      continue

    output[nome_en] = {
      **level_data,
      "offensive_strategies": defesa_info.get("offensive_strategies", [])
    }

  return output

def test_image_analysis():
  image_path = "data/vila_cv_5.jpg"
  analysis = image_analysis(image_path)
  defenses = extract_defense_details(analysis, 'data/defenses_database.json')
  print(json.dumps(analysis, indent=2, ensure_ascii=False))
  print('--' * 40)
  print(defenses)


if __name__ == "__main__":
  test_image_analysis()

# Exemplo de saída sem parse de JSON:
# ```json
# {
#   "cv_level": "6",
#   "defenses": [
#     {"nome": "Canhão", "nível": "7"},
#     {"nome": "Torre de Arqueiras", "nível": "6"},
#     {"nome": "Morteiro", "nível": "4"},
#     {"nome": "Antiaérea", "nível": "4"},
#     {"nome": "Torre do Mago", "nível": "3"}
#   ],
#   "image_analysis": "A vila possui uma disposição centralizada com defesas distribuídas ao longo das paredes internas. As Torres de Arqueiras e Canhões estão posicionados para cobrir todo o perímetro. O Morteiro e a Antiaérea estão mais centralizados, protegendo o Centro de Vila e áreas adjacentes. A Torre do Mago também está perto do centro, reforçando a defesa aérea e terrestre."
# }
# ```

# Exemplo de saída com parse de JSON:
# {
#   "cv_level": "6",
#   "defenses": [
#     {
#       "nome": "Canhão",
#       "nível": "7"
#     },
#     {
#       "nome": "Torre de Arqueiras",
#       "nível": "7"
#     },
#     {
#       "nome": "Morteiro",
#       "nível": "4"
#     },
#     {
#       "nome": "Torre de Magos",    
#       "nível": "3"
#     },
#     {
#       "nome": "Defesa Aérea",
#       "nível": "4"
#     },
#     {
#       "nome": "Antiaérea",
#       "nível": "2"
#     }
#   ],
#   "image_analysis": "A vila tem um layout quadrado com o Centro de Vila no centro, cercado por artilharias como canhões e torres de arqueiras. As defesas estão bem distribuídas para cobertura aérea e terrestre, e o espaço é aproveitado com bom uso de muros para proteger o interior."
# }