import requests
from bs4 import BeautifulSoup
import json
import os

def get_defenses_url():
  '''Busca as URLs de defesa do Clash of Clans no site fandom.com. Retorna um dicionário com o nome da defesa como chave e a URL completa como valor.'''
  
  url = 'https://clashofclans.fandom.com/wiki/Defensive_Buildings/Home_Village'
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  
  defenses_url = {}
  
  table = soup.find('table', { 'class': 'wikitable' })
  
  if not table:
    print("Table not found on the page (get_defenses_url).")
    return defenses_url
  
  all_tr = table.find_all('tr')
  
  if not all_tr:
    print("No rows found in the table (get_defenses_url).")
    return defenses_url
  
  second_row = all_tr[1] if len(all_tr) > 1 else None
  
  if not second_row:
    print("Second row not found in the table (get_defenses_url).")
    return defenses_url
  
  cells = second_row.find_all('td')
  
  if len(cells) < 2:
    print("Not enough cells in the second row (get_defenses_url).")
    return defenses_url
  
  for link_tag in cells[1].find_all('a'):
    name = link_tag.text.strip()
    href = link_tag.get('href', '')
    if name and href:
      full_url = f'https://clashofclans.fandom.com{href}'
      defenses_url[name] = full_url
      
  return defenses_url

def extract_defense_stats(url):
  '''Extrai todos os níveis e atributos da wikitable principal de uma defesa, junto com resumo e estratégias ofensivas.'''
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')

  table = soup.find('table', {'class': 'wikitable'})
  if not table:
    print(f'Nenhuma wikitable encontrada em {url}')
    return {
      'levels': [],
      'summary': [],
      'offensive_strategies': []
    }

  rows = table.find_all('tr')
  if not rows or len(rows) < 2:
    print(f'Tabela sem dados suficientes em {url}')
    return {
      'levels': [],
      'summary': [],
      'offensive_strategies': []
    }

  data = []
  headers = [th.get_text(" ", strip=True) for th in rows[0].find_all('th')]

  for row in rows[1:]:
    cells = row.find_all(['td', 'th'])
    if len(cells) == len(headers):
      item = {
        headers[i]: cells[i].get_text(" ", strip=True)
        for i in range(len(headers))
      }
      data.append(item)

  def get_list_after_id(soup, section_id):
    section = soup.find(id=section_id)
    if section:
      next_ul = section.find_next('ul')
      if next_ul:
        return [li.get_text(" ", strip=True) for li in next_ul.find_all('li')]
    return []

  summary = get_list_after_id(soup, 'Summary')
  offensive_strategies = get_list_after_id(soup, 'Offensive_Strategies')

  return {
    'levels': data,
    'summary': summary,
    'offensive_strategies': offensive_strategies
  }

def build_defenses_database(defenses_url_dict, output_filename='defenses_database.json'):
  '''Recebe um dict {defesa: url} e gera um JSON com os dados extraídos de cada defesa'''
  
  os.makedirs('data', exist_ok=True)
  output_path = os.path.join('data', output_filename)

  database = {}

  for defense_name, url in defenses_url_dict.items():
    print(f'Extraindo dados de: {defense_name}')
    defense_data = extract_defense_stats(url)
    if defense_data:
      database[defense_name] = defense_data
    else:
      print(f'Falha ao extrair dados para {defense_name}')

  with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(database, f, indent=2, ensure_ascii=False)

  print(f'Dados salvos em {output_path}')

def test_without_save():
  defenses_url = get_defenses_url()

  for defense, url in defenses_url.items():
    print(f'Extraindo dados de {defense} ({url})...')
    stats = extract_defense_stats(url)
    print(f'Dados extraídos para {defense}:')
    print(f'Níveis: {stats["levels"]}')
    print(f'Sumário: {stats["summary"]}')
    print(f'Estratégias Ofensivas: {stats["offensive_strategies"]}')
    print('-' * 40)

def init_defenses_database():
  defenses_url = get_defenses_url()
  build_defenses_database(defenses_url, 'defenses_database.json')

if __name__ == '__main__':
  # test_without_save()
  init_defenses_database()
