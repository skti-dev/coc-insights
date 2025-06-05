from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from PIL import Image
from io import BytesIO
import base64

def resize_image_to_base64(image_path: str, max_size: int = 512) -> str:
  with Image.open(image_path) as img:
    img.thumbnail((max_size, max_size))
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

image_chat = ChatOpenAI(model="gpt-4o", max_tokens=512)

def test_image_chain(image_path: str):
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

  return response.content

if __name__ == "__main__":
  image_path = "data/vila_cv_5.jpg"
  response = test_image_chain(image_path)
  print(response)

# Exemplo de saída:
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