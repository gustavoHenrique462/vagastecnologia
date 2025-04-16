import requests
# Cria requisições para pegar o HTTP
from bs4 import BeautifulSoup
# Faz o parsing do HTML e permite extrair dados usando seletores
import pandas as pd
# Estrutura os dados em tabelas (DataFrame), facilita análise e exibição
import matplotlib.pyplot as plt
# Cria gráficos (como gráfico de barras com localizações)
import streamlit as st
# Cria a interface web interativa (dashboard)
from collections import Counter
# Conta quantas vezes cada palavra aparece em uma lista


url = 'https://www.vagas.com.br/vagas-de-tecnologia'

# Definindo headers para simular um navegador e evitar bloqueios
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0'
}


# Função para extrair as vagas
@st.cache_data(show_spinner=True)
def extrair_dados():
    # Fazendo a requisição HTTP para a página
    resposta = requests.get(url, headers=headers)

    # Verificando se a requisição foi bem-sucedida
    if resposta.status_code != 200:
        st.warning(f"Erro na requisição: {resposta.status_code}")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro

    # Transformando o conteúdo HTML da página em um objeto BeautifulSoup
    soup = BeautifulSoup(resposta.content, 'html.parser')

    # Lista para armazenar os dados de cada vaga
    dados = []

    # Encontrando todos os blocos de vaga
    blocos_vagas = soup.find_all('h2')

    # Iterando sobre cada bloco de vaga para coletar os dados
    for bloco in blocos_vagas:
        # Captura todos os títulos da vaga
        titulos = bloco.find_all('h3', class_='chakra-heading')
        titulo_text = titulos[0].text.strip() if titulos else 'Não informado'

        # Captura todas as empresas
        empresas = bloco.find_all('span', class_='emprVaga')
        empresa_text = empresas[0].text.strip(
        ) if empresas else 'Não informado'

        # Captura todos os locais de trabalho
        locais = bloco.find_all('span', class_='vaga-local')
        local_text = locais[0].text.strip() if locais else 'Não informado'

        # Captura todos os requisitos
        requisitos = bloco.find_all('p')
        requisito_text = requisitos[0].text.strip(
        ) if requisitos else 'Não informado'

        # Adiciona as informações da vaga à lista de dados
        dados.append({
            'Título': titulo_text,
            'Empresa': empresa_text,
            'Localização': local_text,
            'Requisitos': requisito_text
        })

    # Convertendo a lista de dados para um DataFrame
    return pd.DataFrame(dados)


# Configuração do Streamlit
st.set_page_config(page_title="Painel de Vagas - Vagas.com", layout="wide")
st.title("💼 Painel de Vagas - Vagas.com")

# Extraindo os dados das vagas
df = extrair_dados()

# Verificando se os dados estão vazios
if df.empty:
    st.warning("Nenhuma vaga encontrada. Verifique se a estrutura do site mudou.")
else:
    # Exibindo a tabela de vagas
    st.subheader(" Tabela de Vagas")
    st.dataframe(df)

    # Gráfico de barras - Cidades com mais vagas
    st.subheader(" Cidades com Mais Vagas")
    cidades = df['Localização'].value_counts()
    fig, ax = plt.subplots()
    cidades.plot(kind='bar', ax=ax, color='teal')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Contagem de palavras mais comuns nos títulos
    st.subheader(" Palavras Mais Usadas nos Títulos")
    palavras = ' '.join(df['Título']).lower().split()
    mais_comuns = Counter(palavras).most_common(10)
    palavras_df = pd.DataFrame(mais_comuns, columns=['Palavra', 'Frequência'])
    st.dataframe(palavras_df)

    # Contagem de palavras mais comuns nos requisitos
    st.subheader(" Requisitos Mais Comuns")
    todos_requisitos = ' '.join(df['Requisitos']).lower().split()
    requisitos_comuns = Counter(todos_requisitos).most_common(10)
    requisitos_df = pd.DataFrame(requisitos_comuns, columns=[
                                 'Requisito', 'Frequência'])
    st.dataframe(requisitos_df)
