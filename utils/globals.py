import requests
from bs4 import BeautifulSoup
import json
import os

def get_levels(soup, url): 
  '''Extrai os níveis de uma página da Fandom do Clash of Clans.'''
  result = []
  
  if not url:
    print('URL não fornecida.')
    return result
  
  if not soup:
    print(f'Erro ao processar a página: {url}')
    return result
  
  statistics_div = soup.find('div', class_='stats-background')
  if not statistics_div:
    print(f'Div .stats-background não encontrada em {url}')
    return result

  tables = statistics_div.find_all('table', class_='wikitable')
  if not tables:
    print(f'Nenhuma wikitable encontrada na div .stats-background em {url}')
    return result

  for table in tables:
    rows = table.find_all('tr')
    if not rows or len(rows) < 2:
      continue

    headers = [th.get_text(" ", strip=True) for th in rows[0].find_all('th')]
    for row in rows[1:]:
      cells = row.find_all(['td', 'th'])
      if len(cells) == len(headers):
        item = {
          headers[i]: cells[i].get_text(" ", strip=True)
          for i in range(len(headers))
        }
        result.append(item)
        
  return result

def get_list_after_id(soup, section_id):
  '''Extrai uma lista de itens após um ID específico em uma página da Fandom do Clash of Clans.'''
  section = soup.find(id=section_id)
  if section:
    next_ul = section.find_next('ul')
    if next_ul:
      return [li.get_text(" ", strip=True) for li in next_ul.find_all('li')]
  return []

def extract_stats(url, get_offensive_strategies=True):
  '''Extrai dados de uma página da Fandom do Clash of Clans, incluindo níveis, resumo e estratégias ofensivas.'''
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')

  result = {
    'levels': [],
    'summary': [],
  }

  result['levels'] = get_levels(soup, url)

  result['summary'] = get_list_after_id(soup, 'Summary')
  
  if get_offensive_strategies:
    result['offensive_strategies'] = []

    for sid in ['Offensive_Strategies', 'Offensive_Strategy', 'Strategy_and_Tips', 'Strategies_and_Tips', 'Offensive']:
      result['offensive_strategies'] = get_list_after_id(soup, sid)
      if result['offensive_strategies']:
        break
  else:
    result['number_of_buildings'] = 1 if 'Army_Camp' not in url else 4
    

  return result

def build_database(url_dict, output_filename='database.json', get_offensive_strategies=True):
  '''Recebe um dict {name: url} e gera um JSON com os dados extraídos de cada URL.'''
  
  os.makedirs('data', exist_ok=True)
  output_path = os.path.join('data', output_filename)

  database = {}

  for name, url in url_dict.items():
    print(f'Extraindo dados de: {name}')
    data = extract_stats(url=url, get_offensive_strategies=get_offensive_strategies)
    if data:
      database[name] = data
    else:
      print(f'Falha ao extrair dados para {name}')

  with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(database, f, indent=2, ensure_ascii=False)

  print(f'Dados salvos em {output_path}')