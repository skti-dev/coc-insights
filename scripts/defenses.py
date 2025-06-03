import requests
from bs4 import BeautifulSoup
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.globals import extract_stats, build_database

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

def test_without_save():
  defenses_url = get_defenses_url()

  for defense, url in defenses_url.items():
    print(f'Extraindo dados de {defense} ({url})...')
    stats = extract_stats(url)
    print(f'Dados extraídos para {defense}:')
    print(f'Níveis: {stats["levels"]}')
    print(f'Sumário: {stats["summary"]}')
    print(f'Estratégias Ofensivas: {stats["offensive_strategies"]}')
    print('-' * 40)

def init_defenses_database():
  defenses_url = get_defenses_url()
  build_database(defenses_url, 'defenses_database.json')

if __name__ == '__main__':
  # test_without_save()
  init_defenses_database()
