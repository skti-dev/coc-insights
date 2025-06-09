import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.st_utils import setup_sidebar

st.set_page_config(page_title="Referências", page_icon="📚", layout="wide")

st.title("📚 Referências utilizadas")

st.markdown("""
Esta página contém a maioria das URLs utilizadas como base para os dados extraídos via web scraping relacionados ao Clash of Clans.

**Atenção:** muitas das URLs utilizadas foram extraídas de tabelas dentro do site [Clash of Clans Wiki](https://clashofclans.fandom.com/wiki/Clash_of_Clans_Wiki) e por isso, não se encontram aqui.

### 🏰 Vila Principal
- [Tropas, Heróis, Feitiços, etc.](https://clashofclans.fandom.com/wiki/Army)
- [Defesas](https://clashofclans.fandom.com/wiki/Defensive_Buildings/Home_Village)
- [Acampamento](https://clashofclans.fandom.com/wiki/Army_Camp/Home_Village)
- [Fábrica de Feitiços](https://clashofclans.fandom.com/wiki/Spell_Factory)
- [Quartéis](https://clashofclans.fandom.com/wiki/Barracks)
- [Laboratório](https://clashofclans.fandom.com/wiki/Laboratory)
- [Hero Hall](https://clashofclans.fandom.com/wiki/Hero_Hall)
- [Ferreiro](https://clashofclans.fandom.com/wiki/Blacksmith)
- [Oficina](https://clashofclans.fandom.com/wiki/Workshop)
- [Pet House](https://clashofclans.fandom.com/wiki/Pet_House)
- [Fábrica de Feitiços Sombrio](https://clashofclans.fandom.com/wiki/Dark_Spell_Factory)

### 📈 Outras fontes
- [Atualizações e eventos](https://supercell.com/en/games/clashofclans/pt/blog/)
- [Página principal da Wiki](https://clashofclans.fandom.com/wiki/Clash_of_Clans_Wiki)

---

Se novas fontes forem adicionadas ao projeto, elas aparecerão aqui.
""")

setup_sidebar()
