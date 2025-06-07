import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.globals import extract_stats, build_database

def get_army_buildings_urls():
  '''Retornar URLs do acampamento, fábrica de feitiços, quartéis e laboratório do Clash of Clans.'''
  urls = {
    'army_camp': 'https://clashofclans.fandom.com/wiki/Army_Camp/Home_Village',
    'spell_factory': 'https://clashofclans.fandom.com/wiki/Spell_Factory',
    'barracks': 'https://clashofclans.fandom.com/wiki/Barracks',
    'laboratory': 'https://clashofclans.fandom.com/wiki/Laboratory'
  }
  return urls

def test_without_save():
  army_buildings_url = get_army_buildings_urls()

  for army_building, url in army_buildings_url.items():
    print(f'Extraindo dados de {army_building} ({url})...')
    stats = extract_stats(url=url, get_offensive_strategies=False)
    stats['number_of_buildings'] = 1 if army_building != 'army_camp' else 4

    print(f'Dados extraídos para {army_building}:')
    print(f'Níveis: {stats["levels"]}')
    print(f'Sumário: {stats["summary"]}')
    print(f'Número de construções: {stats["number_of_buildings"]}')
    print('-' * 40)
    
def init_army_buildings_database():
  army_buildings_url = get_army_buildings_urls()
  build_database(army_buildings_url, output_filename='army_buildings_database.json', get_offensive_strategies=False)
    
if __name__ == '__main__':
  # test_without_save()
  init_army_buildings_database()