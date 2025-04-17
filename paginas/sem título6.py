# %% [1] Importando os pacotes e carregando os dados, etc
# Importando pacotes
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly as pt
import plotly.express as px
import plotly.graph_objects as go

# Carregando dados
from funcoes.tratamento import TratamentoDados

tratador = TratamentoDados()

df_migracao = tratador.retornar_migracao()

# %% Título, e settings

st.markdown("""
    <div style="text-align: center;">
        <h1> Análise dos Salários </h1>
""", unsafe_allow_html=True)

st.markdown("""
Está curioso(a) para saber quanto ganham os profissionais da área que pensa em entrar? 
""")

gradientes = {
    'Rosa': 'PuRd',       # Cores vermelhas
    'Laranja': 'Oranges', # Cores laranja
    'Tomate': 'Reds',     # Cores tomate
    'Verde': 'Greens',    # Cores verdes
    'Azul': 'Blues',      # Cores azuis
    'Cinza': 'Greys'      # Cores cinzas
}

# Sidebar para escolha da cor
with st.sidebar.expander("Escolha a cor para os gráficos 🎨", expanded=True):
    cor_nome = st.selectbox('Escolha uma cor de preferência:',
                           ['Rosa', 'Laranja', 'Tomate', 'Verde', 'Azul', 'Cinza'])
    cor_gradiente = gradientes[cor_nome]

# Templates carregados
template_graph = st.session_state.get("template_graph", "white")
template_plotly = st.session_state.get("template_plotly", "plotly_dark")

if template_graph == "white":
    letras_sns = "black"

else:
    letras_sns = "white"

# %% dicionario(s)

dic_uni2 = {
        "Região de Migração": (
        "A tabela revela a distribuição dos profissionais por região de origem e localização atual, mostrando uma forte concentração nas regiões mais desenvolvidas do Brasil. "
        "A região Sudeste destaca-se com a maior quantidade de profissionais, com 121 oriundos dessa região e 235 de outras. Isso sugere que o Sudeste é um polo central tanto "
        "para a origem quanto para a atual localização dos profissionais, atraindo um grande número de talentos de diversas partes do país. Além disso, o Sudeste é também a "
        "principal região de destino, com destaque para profissionais provenientes de Nordeste e Centro-Oeste.<br><br>"
        
        "O Nordeste tem uma distribuição mais equilibrada, com 29 profissionais oriundos da própria região e 135 de outras áreas. Isso demonstra uma migração considerável para o "
        "Nordeste, que pode ser explicada por fatores como o crescimento de setores e a busca por novas oportunidades nesse território. Já o Sul tem uma distribuição similar, "
        "com 81 profissionais atualmente na região e 58 oriundos de outros locais. A presença de profissionais do Centro-Oeste na região Sul também indica um movimento migratório, "
        "possivelmente em busca de melhores oportunidades de trabalho.<br><br>"
        
        "Por outro lado, as regiões Centro-Oeste e Norte mostram uma concentração maior de profissionais locais. O Centro-Oeste tem 22 profissionais em sua própria região e "
        "12 oriundos de outras áreas, enquanto o Norte tem 17 na região e 16 provenientes de outras. Essas duas regiões tendem a manter uma maior parte de sua força de trabalho "
        "local, com uma mobilidade migratória mais baixa. A região Exterior tem uma representação menor, com destaque para a presença de profissionais provenientes do Sudeste e "
        "Nordeste."
        ),
    }
            
# %% graficos

if 'preguiça' == 'preguiça':
    tabela_migracao = pd.crosstab(df_migracao['Região de Origem'], df_migracao['Região Atual'])

    # Normalize the table to get proportions
    tabela_migracao_proporcional = tabela_migracao.div(tabela_migracao.sum(axis=1), axis=0)

    # Let the user choose between Proporção and Números Absolutos
    opcao_selecao = st.radio('Escolha a versão para visualização:', 
                             ('Proporção', 'Números Absolutos'))

    # Conditional logic to set the table to display based on the user choice
    if opcao_selecao == 'Proporção':
        tabela_exibicao = tabela_migracao_proporcional
        titulo_grafico = 'Região de Origem vs Região Atual (Proporção)'
        fmt = ".2f"  # Format for proportions
    else:
        tabela_exibicao = tabela_migracao
        titulo_grafico = 'Região de Origem vs Região Atual (Contagem)'
        fmt = "d"  # Format for absolute counts
    
    # Create the heatmap
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(tabela_exibicao, annot=True, cmap=cor_gradiente, fmt=fmt, ax=ax)
    
    # Customize labels and font sizes
    ax.set_title(titulo_grafico, fontsize=16, color=letras_sns)
    ax.set_xlabel('Região Atual', fontsize=12, color=letras_sns)
    ax.set_ylabel('Região de Origem', fontsize=12, color=letras_sns)
    ax.tick_params(axis='x', colors=letras_sns)  # x-axis ticks color
    ax.tick_params(axis='y', colors=letras_sns)  # y-axis ticks color
    fig.patch.set_facecolor(template_graph)  # Set background color to black
    
    # Show the plot
    st.pyplot(fig)


    #st.subheader('Tabela de Migração entre Regiões')
    #st.write(tabela_migracao)
    st.markdown(dic_uni2['Região de Migração'], unsafe_allow_html=True)
    
va_pizza = st.selectbox('Escolha uma variável para o gráfico:', sorted(lista_estados))