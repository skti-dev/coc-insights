import requests
from bs4 import BeautifulSoup
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.globals import extract_stats, build_database

def get_army_url():
  '''Busca as URLs do exército do Clash of Clans no site fandom.com. Retorna um dicionário com o nome da tropa como chave e a URL completa como valor.'''
  
  url = 'https://clashofclans.fandom.com/wiki/Army'
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  
  army_url = {}
  
  table = soup.find('table', { 'class': 'wikitable' })
  
  if not table:
    print("Table not found on the page (get_army_url).")
    return army_url
  
  all_tr_but_first = table.find_all('tr')[1:]
  
  if not all_tr_but_first:
    print("No rows found in the table (get_army_url).")
    return army_url
  
  for row in all_tr_but_first:
    cells = row.find_all('td')
  
    if len(cells) < 2:
      continue
  
    for link_tag in cells[1].find_all('a'):
      name = link_tag.text.strip()
      href = link_tag.get('href', '')
      if name and href:
        full_url = f'https://clashofclans.fandom.com{href}'
        army_url[name] = full_url
        
  return army_url
  
def test_without_save():
  army_url = get_army_url()

  for army, url in army_url.items():
    print(f'Extraindo dados de {army} ({url})...')
    stats = extract_stats(url)
    print(f'Dados extraídos para {army}:')
    print(f'Níveis: {stats["levels"]}')
    print(f'Sumário: {stats["summary"]}')
    print(f'Estratégias Ofensivas: {stats["offensive_strategies"]}')
    print('-' * 40)
  
def init_army_database():
  army_url = get_army_url()
  build_database(army_url, 'army_database.json')
    
if __name__ == '__main__':
  # test_without_save()
  init_army_database()