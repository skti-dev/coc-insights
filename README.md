# 🤖 Clash of Clans Assistant

Um assistente inteligente para jogadores de **Clash of Clans**, com conhecimento detalhado sobre tropas, defesas, heróis, feitiços, estratégias de ataque e atualizações do jogo. Desenvolvido com **LangChain**, **OpenAI GPT-4o**, **Streamlit** e uma base de dados construída via **web scraping**.

---

## 📸 Demonstração
![resposta_com_analise_de_imagem](https://github.com/user-attachments/assets/b7c13b7f-5382-40dd-a596-acc3114a867f)
![resposta_sobre_a_vila](https://github.com/user-attachments/assets/fe47fc0f-ad57-4499-bcd7-a0f5d920ecd1)
![resposta_ultimas_noticias](https://github.com/user-attachments/assets/bc905a09-5db0-4578-ad98-33c6e3cd3065)
![resposta_pergunta_sem_relacao](https://github.com/user-attachments/assets/49461151-a41f-4f90-9a41-09d116d5fb0f)
![tela_avisos_importantes](https://github.com/user-attachments/assets/0d4da962-5b7d-424c-a1e2-f3eb1a6aa1a3)
![tela_referencias](https://github.com/user-attachments/assets/843c2e03-d9be-4fbc-97f5-225210a6d87c)
![exemplo_db](https://github.com/user-attachments/assets/587bb1bf-2653-4588-969b-8d5cc3acfb57)
![exemplo_langsmith](https://github.com/user-attachments/assets/1f986ddf-17e6-4231-a860-ac4ade84bf2c)

---

## 🧠 Sobre o Projeto

Este projeto tem como objetivo oferecer uma interface interativa para que jogadores possam tirar dúvidas específicas sobre Clash of Clans — seja sobre **estratégias de ataque**, **níveis de tropas por Centro de Vila (CV)**, **eventos/atualizações recentes**, ou até mesmo **análise de imagens** com informações visuais do jogo.

O diferencial do projeto está na combinação de:

- **Classificação automática de perguntas por categoria**
- **Roteamento dinâmico de prompts para cadeias especializadas (LangChain)**
- **Persistência de histórico em SQLite**
- **Interação via chat com streaming de resposta**
- **Upload e análise de imagens com GPT-4o**
* **Entender o contexto da pergunta do usuário**
* **Filtrar dinamicamente as informações relevantes antes de gerar uma resposta**
* **Analisar imagens enviadas pelo jogador para entender o tipo de vila ou disposição das defesas**
* **Buscar notícias atualizadas na web, quando necessário, usando _tools_ integradas via LangChain**

---

## 🚀 Destaques Técnicos

### 🔍 Filtragem de Conhecimento Inteligente

Antes de enviar qualquer prompt ao modelo de linguagem, o sistema realiza uma **filtragem prévia da base de dados** com base em dois critérios principais:

1. **Conteúdo da pergunta**: O texto do usuário é analisado para identificar os tópicos relevantes (ex: tropas, CV, defesas).
2. **Imagem enviada (se houver)**: Se uma imagem for incluída, ela é processada pelo modelo para identificar elementos visuais (como Torres Inferno, Layouts, etc.), permitindo **respostas mais direcionadas ao contexto da vila exibida** .

Essa filtragem garante que o modelo tenha acesso **somente às informações relevantes**, evitando respostas genéricas ou equivocadas.

### 🌐 Uso de Tools para Notícias Dinâmicas

A chain responsável por perguntas sobre **novidades e atualizações** do jogo utiliza a funcionalidade de **tools do LangChain**, que permite:

- Consultar mecanismos de busca em tempo real
- Capturar trechos de notícias e artigos relevantes
- Integrar a resposta com base no conteúdo encontrado na web

Esse recurso é ativado **somente quando a base de dados local não possui informações suficientes**, o que garante um bom equilíbrio entre precisão e atualidade.

Esses diferenciais tornam o assistente não apenas uma ferramenta útil, mas também uma **demonstração prática de boas práticas no uso de LLMs** , incluindo roteamento, uso de ferramentas, contexto multimodal e persistência de sessão.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia                                 | Descrição                                                           |
| ------------------------------------------ | ------------------------------------------------------------------- |
| [Streamlit](https://streamlit.io)          | Interface web interativa, leve e rápida                             |
| [LangChain](https://www.langchain.com)     | Framework de orquestração para LLMs                                 |
| [OpenAI GPT-4o](https://openai.com/gpt-4o) | Modelo de linguagem multimodal usado para respostas e classificação |
| [SQLite](https://sqlite.org)               | Banco de dados local para armazenamento do histórico                |
| [Pillow](https://python-pillow.org)        | Manipulação de imagens (upload, leitura, salvamento)                |
| Web Scraping                               | Coleta dos dados técnicos sobre o jogo diretamente da Wiki          |
| [LangSmith](https://smith.langchain.com/)  | Logs e entendimento detalhado dos processos das chains              |

---

## 🔍 Funcionalidades

- 📂 **Classificação de perguntas**: O modelo determina se o usuário está perguntando sobre ataque, CV, atualizações ou algo genérico.
- 🧩 **Roteamento inteligente**: Cada categoria é processada por uma chain específica.
- 💬 **Chat com memória persistente**: Cada sessão de usuário é registrada e salva.
- 📷 **Upload de imagem com análise contextual**: O usuário pode enviar imagens para análise contextual (ex: layout de vila).
- 🧽 **Limpeza de histórico pela interface**.
- 🧵 **Respostas com streaming em tempo real.**

---

## ⚙️ Como Executar Localmente

```bash
# Clone o repositório
git clone https://github.com/skti-dev/coc-insights.git
cd coc-insights

# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Crie um arquivo .env
touch .env

# Veja o arquivo env-example.txt para preencher o seu próprio .env

# Rode os arquivos dentro da pasta 'scripts' para fazer o web scraping e armazenar dentro de /data
python army_buildings.py
python army.py
python defenses.py

# A aplicação já está pronta e pode ser iniciada pelo comando do streamlit
streamlit run
```

## 📎 Referências

- [Clash of Clans Fandom Wiki](https://clashofclans.fandom.com)
- [LangChain Docs]()
- [Streamlit Docs]()
- [LangSmith Docs](https://docs.smith.langchain.com/)

## 💡 Próximos Passos

- [ ] Melhorar a análise de imagem (classificação automática de vilas);
- [ ] Implementar feedback de usuário por resposta;
- [ ] Suporte para múltiplos idiomas;
- [ ] Dashboard de estatísticas de uso;

## 📬 Contato

Criado por **Augusto Seabra** — [LinkedIn](https://linkedin.com/in/augusto-seabra-desenvolvedor)
