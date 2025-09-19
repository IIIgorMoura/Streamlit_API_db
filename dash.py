import streamlit as st
import pandas as pd
import plotly.express as px
# sidebar de troca de telas e filtros
from streamlit_option_menu import option_menu
# link com o banco (código no query.py)
from query import conexao

# *** Primeira Consulta e Atualização
# * Consulta SQL (É a mesma seleção que é feita no MySQL (sem ;))
query = 'SELECT * FROM tb_carros'
# Carregar os dados para a var 'df'
df = conexao(query)

# * Atualização (Para não precisar dar f5 na página)
# botao
if st.button('Atualizar'):
    df = conexao(query)

# -----------

# *** Estrutura de Filtro Lateral
filtro_marca = st.sidebar.multiselect(
    "Marca Selecionada", 
    options=df["marca"].unique(),
    # já trazer tudo selecionado
    default=df['marca'].unique()
)

# Modelo
filtro_modelo = st.sidebar.multiselect(
    options=df['modelo'].unique(),
    default=df['modelo'].unique()
)

# Ano
min_ano = int(df["ano"].min())
max_ano = int(df["ano"].max())

filtro_ano = st.sidebar.slider(
    "Ano do Veículo", 
    min_value=min_ano, 
    max_value=max_ano, 
    value=(min_ano, max_ano), 
    step=1
)

# Valor
min_valor = float(df["valor"].min())
max_valor = float(df["valor"].max())

filtro_valor = st.sidebar.slider(
    "Valor do Veículo", 
    min_value=min_valor, 
    max_value=max_valor, 
    value=(min_valor, max_valor), 
    step=1000.0
)

# Vendas
min_vendas = int(df["numero_vendas"].min())
max_vendas = int(df["numero_vendas"].max())

filtro_vendas = st.sidebar.slider(
    "Número de Vendas", 
    min_value=min_vendas, 
    max_value=max_vendas, 
    value=(min_vendas, max_vendas), 
    step=1
)


# Cor
filtro_cor = st.sidebar.multiselect(
    "Cor Selecionada",
    options=df["cor"].unique(),
    default=df["cor"].unique()
)


# *** Verificacao da aplicação dos filtros
df_selecionado = df[
    (df["marca"].isin(filtro_marca)) &
    (df["modelo"].isin(filtro_modelo)) &
    (df["ano"].isin(filtro_ano)) &
    (df["cor"].isin(filtro_cor)) &

    (df['numero_vendas'] >= filtro_vendas[0]) & (df['numero_vendas'] <= filtro_vendas[1]) &
    
    (df["valor"] >= filtro_valor[0]) & (df["valor"] <= filtro_valor[1]) & 

    (df["numero_vendas"] >= filtro_vendas[0]) & (df["numero_vendas"] <= filtro_vendas[1])
]



# *** Dashboard
def PaginaInicial():

    # Cards de principais valores

    # expande para selecionar as opções
    with st.expander("Tabela de Carros"):
        exibicao = st.multiselect(
                "Filtro",
                df_selecionado.columns,
                default=[],
                # identificadores
                key="Filtro_Exibicao"
            )
        if exibicao:
            st.write(df_selecionado[exibicao])
