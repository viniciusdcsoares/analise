# -- coding: utf-8 --
"""
Created on Fri Nov 29 00:30:22 2024

@author: zaywa
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly as pt
import plotly.express as px

link = 'https://raw.githubusercontent.com/ricardorocha86/Datasets/refs/heads/master/State_of_data_BR_2023_Kaggle%20-%20df_survey_2023.csv'
df_o = pd.read_csv(link)
df = df_o.copy()

df.rename(columns={"('P1_a ', 'Idade')": 'Idade', "('P1_c ', 'Cor/raca/etnia')": 'Etnia',
                   "('P1_b ', 'Genero')": 'Gênero', "('P2_f ', 'Cargo Atual')": 'Cargo',
                   "('P2_h ', 'Faixa salarial')": 'Faixa Salarial', "('P2_g ', 'Nivel')": 'Nível',
                   "('P1_l ', 'Nivel de Ensino')": 'Escolaridade', "('P1_m ', 'Área de Formação')": 'Área',
                   "('P2_i ', 'Quanto tempo de experiência na área de dados você tem?')": 'Experiência'
                   }, inplace=True)
df['Contagem'] = 1


# Definição das regiões
norte = ['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO']
nordeste = ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE']
centro = ['DF', 'GO', 'MS', 'MT']
sudeste = ['ES', 'MG', 'RJ', 'SP']
sul = ['PR', 'RS', 'SC']

categorias = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]

# Função para mapear estados para regiões
def estado_para_regiao(coluna_antiga, coluna_nova, df_migracao):
    condicao = [
        df_migracao[coluna_antiga].str.contains('|'.join(norte), na=False),
        df_migracao[coluna_antiga].str.contains('|'.join(nordeste), na=False),
        df_migracao[coluna_antiga].str.contains('|'.join(centro), na=False),
        df_migracao[coluna_antiga].str.contains('|'.join(sudeste), na=False),
        df_migracao[coluna_antiga].str.contains('|'.join(sul), na=False)
    ]
    df_migracao[coluna_nova] = np.select(condicao, categorias, default='Exterior')
    return df_migracao

# Supondo que o dataframe 'df' já tenha sido carregado anteriormente
df_migracao = df[["('P1_k ', 'Regiao de origem')", "('P1_i ', 'Estado onde mora')"]]
df_migracao.dropna(inplace=True)
df_migracao = df_migracao[df_migracao["('P1_k ', 'Regiao de origem')"] != df_migracao["('P1_i ', 'Estado onde mora')"]]

# Renomear as colunas para algo mais acessível
antigas = ["('P1_k ', 'Regiao de origem')", "('P1_i ', 'Estado onde mora')"]
novas = ["Região de Origem", "Região Atual"]

for antiga, nova in zip(antigas, novas):
    df_migracao = estado_para_regiao(antiga, nova, df_migracao)

###############

st.title("Trabalho Final do MiniCurso Python para Inteligência Artificial")

st.markdown("""

## Análise Descritiva da Base de Dados - Perfil do Profissional de Dados no Brasil
    
""")

st.markdown("---")


###############Opções de Preferencia##########

st.markdown("""
### Opções de Preferência 🎨

Antes das análiese, temos uma boa noticia para te dar: 

Você tem a possibilidade de escolher alguns detalhes para personalizar os gráficos gerados. 📊

Nada muito complicado, apenas um toque para tornar a experiência ainda mais sua! 😊

À esquerda da página, escolha a cor que mais agrada e aproveite os gráficos de forma personalizada! 🌈
""")


mapa_cores = {
    'Rosa': '#FF69B4',  # Rosa Intermediário (HotPink)
    'Laranja': '#FF8C00', # Laranja
    'Tomate': '#FF6347',  # Tomate
    'Verde': '#32CD32',   # Verde
    'Azul': '#4682B4',    # Azul Escuro (SteelBlue)
    'Cinza': '#808080'    # Cinza
}

mapa_cmap = {
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

    cor = mapa_cores[cor_nome]  # Cor para os gráficos
    corm = mapa_cmap[cor_nome]  # Cores do cmap# Exibindo a cor selecionada na tela principal

st.markdown("---")


###############Descrição Geral da Base##########################

st.markdown("""
### Descrição Geral da Base🔍

Antes de mais nada vamos lhe fornecer uma visão 
geral dos dados, para que assim você possa melhor 
percorrer pelas secções a seguir. 🚀

A base se refere ao **Perfil do Profissional de Dados 
no Brasil**. Sendo composta por de 5 293 
indivíduos e 400 variáveis, mas, devido ao tempo, 
nossas análises referem-se apenas a um subconjunto 
dessas variáveis. 

Esse subconjunto incluem as seguintes variáveis 
presentes na base:

- *Área de Formação*: A área de formação acadêmica desses profissionais.
- *Cargo*: Cargo atual ocupado pelos profissionais de dados.
- *Etnia*: Cor/raça/etnia dos participantes.
- *Escolaridade*: Nível de escolaridade dos profissionais.
- *Estado onde Mora*: Estado em que o profissional reside atualmente.
- *Experiência*: O tempo de experiência na área de dados.
- *Faixa Salarial*: Divisão da faixa salarial dos profissionais.
- *Gênero*: Distribuição de gênero entre os profissionais.
- *Idade*: Faixa etária dos profissionais de dados.
- *Nível*: Nível de experiência ou senioridade dentro da área de dados.
- *Região de Origem*: Local onde o profissional nasceu ou cresceu.

Essas variáveis ajudam a criar um panorama detalhado 
sobre a formação e o perfil dos profissionais de 
dados no Brasil, permitindo análises mais 
profundas e insights valiosos sobre esse setor. 💡


""")

st.markdown("---")

###############Analises Univariada##########################

st.markdown("""
# Análise Univariada 📈

Nessa secção você pode visualizar alguns 
gráficos, que propomos para a análise 
univariada das variáveis da base. Além disso, 
fornecemos também uma análise acerca dos 
gráficos gerados, para que você não 
precise ter esse trabalho. 🧠

Tudo o que vai precisar fazer é selecionar a 
variável desejada e se divertir com o processo!🙃

""")

###############Interpretação dos Gráificos de Pizza##########################

idade1 = "A distribuição etária dos profissionais no mercado de dados no Brasil mostra uma predominância de jovens na faixa etária de 20 a 30 anos, que representam uma parcela significativa da base. A maior concentração está na faixa de 26 anos, com 323 profissionais (6.1%), seguida pela faixa de 27 anos, com 374 profissionais (7.1%), indicando uma forte presença de profissionais em início de carreira ou em transição para posições mais consolidadas. As faixas etárias mais altas, como 50 anos ou mais, têm uma representatividade bem menor, com apenas 1 a 2 profissionais em cada faixa etária acima de 60 anos, evidenciando uma baixa participação de profissionais mais velhos no setor. Esse cenário reflete um mercado de dados mais jovem, com a maioria dos profissionais em fases iniciais ou intermediárias de sua carreira."

faixasalarial1 = "A distribuição salarial no mercado de dados no Brasil revela uma clara concentração nas faixas intermediárias, com destaque para o intervalo de 8 001 a 12 000 reais, com 1 026 profissionais, seguido por 4 001 a 6 000 reais, com 745 profissionais, e 12 001 a 16 000 reais, com 650 profissionais. As faixas salariais mais altas, como 16 001 a 20 000 reais (328 profissionais) e Acima de 40 000  reais (72 profissionais), têm uma presença mais modesta, sugerindo que apenas uma pequena parcela dos profissionais alcançam esses valores. Já as faixas mais baixas, como Menos de 1 000 reais (30 profissionais), têm uma representação reduzida, indicando que a maioria dos profissionais está concentrada nas faixas intermediárias ou mais altas."

experiencia1 = "A experiência também é um fator importante nesse mercado. Cerca de 40% dos profissionais (aproximadamente 2.000 indivíduos) possuem entre 1 e 4 anos de experiência, o que mostra que a maior parte da base está em fase de formação ou em transição para cargos mais seniores. Esse dado sugere uma alta rotatividade e a constante entrada de novos profissionais no mercado de dados."
experiencia2 = "Outro dado relevante é que 3% (aproximadamente 160 profissionais) são iniciantes, com nenhuma experiência formal na área, mas provavelmente com potencial para crescer à medida que o mercado se expande e a demanda por dados aumenta."
experiencia3 = "Entre os profissionais mais experientes, há um equilíbrio entre as faixas de 4 a 6 anos e 7 a 10 anos de experiência, com um número ligeiramente maior de profissionais na faixa de 4 a 6 anos. Isso indica uma estabilização na distribuição de experiência, com uma concentração significativa de profissionais já consolidados entre 4 e 10 anos de atuação no setor de dados."

regiao1 ="A tabela revela a distribuição dos profissionais por região de origem e localização atual, mostrando uma forte concentração nas regiões mais desenvolvidas do Brasil. A região Sudeste destaca-se com a maior quantidade de profissionais, com 121 oriundos dessa região e 235 de outras. Isso sugere que o Sudeste é um polo central tanto para a origem quanto para a atual localização dos profissionais, atraindo um grande número de talentos de diversas partes do país. Além disso, o Sudeste é também a principal região de destino, com destaque para profissionais provenientes de Nordeste e Centro-Oeste."
regiao2 ="O Nordeste tem uma distribuição mais equilibrada, com 29 profissionais oriundos da própria região e 135 de outras áreas. Isso demonstra uma migração considerável para o Nordeste, que pode ser explicada por fatores como o crescimento de setores e a busca por novas oportunidades nesse território. Já o Sul tem uma distribuição similar, com 81 profissionais atualmente na região e 58 oriundos de outros locais. A presença de profissionais do Centro-Oeste na região Sul também indica um movimento migratório, possivelmente em busca de melhores oportunidades de trabalho."
regiao3 ="Por outro lado, as regiões Centro-Oeste e Norte mostram uma concentração maior de profissionais locais. O Centro-Oeste tem 22 profissionais em sua própria região e 12 oriundos de outras áreas, enquanto o Norte tem 17 na região e 16 provenientes de outras. Essas duas regiões tendem a manter uma maior parte de sua força de trabalho local, com uma mobilidade migratória mais baixa. A região Exterior tem uma representação menor, com destaque para a presença de profissionais provenientes do Sudeste e Nordeste."

dic_pizza = {
    "Etnia": (
        "A análise da etnia dos profissionais também revela um panorama interessante. "
        "A maioria dos indivíduos na base se identifica como branca, representando 65% (3.414) dos participantes. "
        "Em seguida, pardos e pretos somam 32% (1.668), o que representa menos da metade do número de indivíduos identificados como brancos. "
        "Pode-se, assim, afirmar que o mercado de Dados no Brasil está, de forma esmagadora, sendo 'dominado' por brancos.<br><br>"
        
        "Por outro lado, as etnias amarela e indígena têm uma presença mais modesta, representando apenas 3% (159) dos profissionais, "
        "o que pode refletir um padrão demográfico mais restrito, ainda em processo de inclusão em áreas mais tecnológicas."
    ),
    "Gênero": (
        "A distribuição de gênero no mercado de dados no Brasil é predominantemente masculina, com 75% (3.905 profissionais) "
        "se identificando como homens, enquanto 24% (1.293 profissionais) são mulheres. "
        "A presença de profissionais que se identificam com outro gênero é bastante pequena, representando apenas 1% (9 profissionais) da base. "
        "Isso indica uma disparidade significativa entre os gêneros, com a maioria dos cargos ainda sendo ocupada por homens."
    ),
    "Escolaridade": (
        "Em relação à escolaridade, a base de profissionais apresenta uma diversidade interessante. "
        "34% (1.818) dos indivíduos possuem pós-graduação, destacando o alto nível de especialização presente no mercado de dados. "
        "Esse número é similar ao de profissionais com graduação (também 34%, ou 1.798), mostrando que a formação superior continua sendo "
        "um pré-requisito essencial, tanto para cargos de análise quanto para cargos mais técnicos.<br><br>"
        
        "Por outro lado, 2% (105) dos profissionais não possuem graduação, uma porcentagem pequena, mas que pode indicar a presença de "
        "profissionais com trajetórias não convencionais ou autodidatas, especialmente em campos técnicos onde a experiência prática "
        "muitas vezes suplanta a formação acadêmica formal. Já os PhDs ou Doutores representam 4% (210) da base, o que reflete a presença "
        "de especialistas com um nível de formação avançado, muitas vezes voltados para pesquisas, desenvolvimento de novos métodos ou "
        "inovações na área de dados."
    ),
    "Nível": (
        "A distribuição dos níveis de experiência no mercado de dados no Brasil é bastante equilibrada, com *20% (1.046 profissionais)* "
        "em cargos *juniores*, **27% (1.419 profissionais)* em cargos *sêniores*, **26% (1.419 profissionais)* em cargos *plenos* e "
        "*27% (1.436 profissionais)* em cargos *NA*. O fato de haver uma quantidade equivalente de profissionais em cargos **plenos* e "
        "*sêniores* é surpreendente, indicando que a área de dados não só está em constante renovação, mas também mantém um bom equilíbrio "
        "entre profissionais com menos e mais experiência, refletindo uma estabilidade na estrutura de carreiras dentro do setor.<br><br>"
        
        "Além disso, a presença de 27% (1.436 profissionais) com valores faltantes (NA) é uma questão relevante, pois indica uma lacuna "
        "significativa nas informações sobre o nível de experiência de uma parte expressiva dos profissionais. Essa falta de dados claros "
        "prejudica a análise precisa do perfil do mercado, tornando difícil entender a real composição das carreiras no setor."
    ),
    "Cargo": (
        "Devido à similaridade entre algumas profissões, ou por conveniência devido à baixa frequência de observações, agrupamos as profissões "
        "em categorias conforme apresentado na tabela após o texto. "
        "Quase 50% (1 647) dos profissionais dessa base ocupam o cargo de Analista de Dados, o que mostra como essa profissão tem se destacado "
        "e se tornado essencial à medida que mais empresas investem em dados para tomar decisões estratégicas.<br><br>"
        
        "Por outro lado, Estatísticos e Economistas são as profissões com a menor representatividade, somando menos de 1% da base (26) – uma evidência "
        "de que o mercado tem se concentrado mais em habilidades voltadas para a prática e o uso de dados no dia a dia das empresas.<br><br>"
        
        "É interessante notar que, juntos, os cargos de Engenheiro de Dados e Cientista de Dados quase chegam ao número de Analistas de Dados (1 605). "
        "Essa tríade – Analistas, Engenheiros e Cientistas de Dados – responde por mais de 80% da base (3 248), o que revela uma clara tendência: "
        "o mercado está cada vez mais centrado em profissionais que dominam o universo dos dados, seja para analisá-los, estruturá-los "
        "ou transformá-los em insights valiosos."
    )
}


###############Gráificos##########################

st.markdown("""
## Gráficos de pizza!😋🍕😱
""")

va_pizza = st.selectbox('Escolha uma variável para análise:',
                                    sorted(['Etnia', 'Gênero', 'Escolaridade', 'Nível', 'Cargo']))

st.markdown(f"<h3 style='text-align: center'>Gráfico de Setores de {va_pizza}</h3>", unsafe_allow_html=True)


if va_pizza == 'Cargo':
    
    analista = ['Analista de Negócios/Business Analyst', 'Analista de BI/BI Analyst', 'Analista de Dados/Data Analyst', 'Analista de Inteligência de Mercado/Market Intelligence']
    cientista = ['Cientista de Dados/Data Scientist', 'Engenheiro de Machine Learning/ML Engineer/AI Engineer']
    engenheiro = ['Engenheiro de Dados/Arquiteto de Dados/Data Engineer/Data Architect', 'DBA/Administrador de Banco de Dados', 'Analytics Engineer']
    ti = ['Analista de Suporte/Analista Técnico', 'Desenvolvedor/ Engenheiro de Software/ Analista de Sistemas']
    outro = ['Outra Opção', 'Outras Engenharias (não inclui dev)']
    EE = ['Economista', 'Estatístico']
    prof = ['Professor/Pesquisador']
    
    cargo_original = df['Cargo'].value_counts().reset_index(name='Contagem')
    cargo_original.columns = ['Cargo', 'Contagem']

    def categorizar_cargo(cargo):
        if cargo in analista:
            return 'Analista de Dados'
        elif cargo in cientista:
            return 'Cientista de Dados'
        elif cargo in engenheiro:
            return 'Engenheiro de Dados'
        elif cargo in ti:
            return 'Software'
        elif cargo in outro:
            return 'Outra Opção'
        elif cargo in EE:
            return 'EE'
        elif cargo in prof:
            return 'Professor/Pesquisador'
        else:
            return 'Outros'

    cargo_original['Categoria'] = cargo_original['Cargo'].apply(categorizar_cargo)

    # Adicionando uma linha de total
    total_linhas = cargo_original['Contagem'].sum()
    total_row = pd.DataFrame([['Total', total_linhas, 'Total']], columns=['Cargo', 'Contagem', 'Categoria'])
    cargo_original = pd.concat([cargo_original, total_row], ignore_index=True)

    # Ordenando a tabela pela coluna 'Categoria' (segunda coluna)
    cargo_original = cargo_original.sort_values(by='Categoria', ascending=True)

    # Reorganizando as colunas para que 'Contagem' seja a última
    cargo_original = cargo_original[['Cargo', 'Categoria', 'Contagem']]
    
    # Substituindo os cargos para as categorias simplificadas
    df['Cargo'] = df['Cargo'].replace(analista, 'Analista de Dados')
    df['Cargo'] = df['Cargo'].replace(cientista, 'Cientista de Dados')
    df['Cargo'] = df['Cargo'].replace(engenheiro, 'Engenheiro de Dados')
    df['Cargo'] = df['Cargo'].replace(ti, 'Software')
    df['Cargo'] = df['Cargo'].replace(outro, 'Outra Opção')
    df['Cargo'] = df['Cargo'].replace(EE, 'EE')

    # Calculando a contagem de cada cargo após as substituições
    cargo_contagem = df.groupby('Cargo')['Cargo'].count().reset_index(name='Contagem')

    # Gráfico de setores para "Cargo"
    st.subheader(f"Gráfico de Setores de {va_pizza}")
    fig = px.pie(cargo_contagem, values="Contagem", names="Cargo", title="Distribuição de Cargos")
    st.plotly_chart(fig)

    st.markdown(f"<h3 style='text-align: center'>{va_pizza}</h3>", unsafe_allow_html=True)

    # Display dictionary content with line breaks
    st.markdown(dic_pizza[va_pizza], unsafe_allow_html=True)

    st.subheader("Tabela com Quantidades Originais de Cargos")
    st.dataframe(cargo_original)  # Exibe a tabela com os cargos originais sem agrupamento

else: 
    # Pie chart
    fig = px.pie(df, values="Contagem", names=va_pizza)
    #fig.update_layout(title_x=0.5)
    st.plotly_chart(fig)

    # Centered title for va_pizza
    st.markdown(f"<h3 style='text-align: center'>{va_pizza}</h3>", unsafe_allow_html=True)

    # Display dictionary content with line breaks
    st.markdown(dic_pizza[va_pizza], unsafe_allow_html=True)

variavel_selecionada = st.selectbox('Escolha uma variável para análise:',
                                    sorted(['Idade', 'Região', 'Faixa Salarial', 'Experiência']))


if variavel_selecionada == 'Idade':
    
    st.subheader(f"Histograma de {variavel_selecionada}")
    plt.figure(figsize=(18, 6))
    plt.hist(df[variavel_selecionada], edgecolor='black', bins=25, color=cor)
    plt.title(f"Histograma da {variavel_selecionada}")
    plt.xlabel(variavel_selecionada)
    plt.ylabel("Frequência")    
    
    idade_contagem = df['Idade'].value_counts().sort_index()
    
    total_idade = len(df)
    idade_porcentagem = (idade_contagem / total_idade) * 100
    
    tabela_idade = pd.DataFrame({
        'Idade': idade_contagem.index,
        'Contagem': idade_contagem.values,
        'Porcentagem (%)': idade_porcentagem.round(1).values
    })
    
    st.pyplot(plt)
    st.write(idade1)
    st.table(tabela_idade)

elif variavel_selecionada == 'Faixa Salarial':
    ordem_faixa_salarial = df['Faixa Salarial'].value_counts().index.tolist()

    st.subheader('Distribuição de Faixa Salarial')
    
    # Contagem das faixas salariais
    faixa_salarial_contagem = df['Faixa Salarial'].value_counts().sort_index()
    
    # Calculando a porcentagem de cada faixa salarial
    total_faixa = len(df)
    faixa_salarial_porcentagem = (faixa_salarial_contagem / total_faixa) * 100
    
    # Criando um DataFrame com as contagens e porcentagens
    tabela_faixa_salarial = pd.DataFrame({
        'Faixa Salarial': faixa_salarial_contagem.index,
        'Contagem': faixa_salarial_contagem.values,
        'Porcentagem (%)': faixa_salarial_porcentagem.round(1).values
    })
    
    # Plotando o gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=df, x='Faixa Salarial', order=ordem_faixa_salarial, ax=ax, color=cor)

    # Adicionando as porcentagens no gráfico
    for p in ax.patches:
        height = p.get_height()
        percentage = (height / total_faixa) * 100
        ax.text(
            p.get_x() + p.get_width() / 2, height + 1, f'{percentage:.1f}%', 
            ha='center', va='bottom', fontsize=10, color='black'
        )

    ax.set_title('Distribuição de Faixa Salarial', fontsize=16)
    ax.set_xlabel('Faixa Salarial', fontsize=12)
    ax.set_ylabel('Contagem', fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    
    st.pyplot(fig)
    st.write(faixasalarial1)
    st.table(tabela_faixa_salarial)


elif variavel_selecionada == 'Cargo1':
    cargo_original = df['Cargo'].value_counts().reset_index(name='Contagem')
    cargo_original.columns = ['Cargo', 'Contagem']

    # Exibindo a tabela com os cargos originais
    st.subheader("Tabela com Quantidades Originais de Cargos")
    st.dataframe(cargo_original)  # Exibe a tabela com os cargos originais sem agrupamento

    st.write(cargo1)

    analista = ['Analista de Negócios/Business Analyst', 'Analista de BI/BI Analyst', 'Analista de Dados/Data Analyst', 'Analista de Inteligência de Mercado/Market Intelligence']
    cientista = ['Cientista de Dados/Data Scientist', 'Engenheiro de Machine Learning/ML Engineer/AI Engineer']
    engenheiro = ['Engenheiro de Dados/Arquiteto de Dados/Data Engineer/Data Architect', 'DBA/Administrador de Banco de Dados', 'Analytics Engineer']
    ti = ['Analista de Suporte/Analista Técnico', 'Desenvolvedor/ Engenheiro de Software/ Analista de Sistemas']
    outro = ['Outra Opção', 'Outras Engenharias (não inclui dev)']
    EE = ['Economista', 'Estatístico']

    # Substituindo os cargos para as categorias simplificadas
    df['Cargo'] = df['Cargo'].replace(analista, 'Analista de Dados')
    df['Cargo'] = df['Cargo'].replace(cientista, 'Cientista de Dados')
    df['Cargo'] = df['Cargo'].replace(engenheiro, 'Engenheiro de Dados')
    df['Cargo'] = df['Cargo'].replace(ti, 'Software')
    df['Cargo'] = df['Cargo'].replace(outro, 'Outra Opção')
    df['Cargo'] = df['Cargo'].replace(EE, 'EE')

    # Calculando a contagem de cada cargo
    cargo_contagem = df.groupby('Cargo')['Cargo'].count().reset_index(name='Contagem')

    # Gráfico de setores para "Cargo"
    st.subheader(f"Gráfico de Setores de {variavel_selecionada}")
    fig = px.pie(cargo_contagem, values="Contagem", names="Cargo", title="Distribuição de Cargos")
    st.plotly_chart(fig)

elif variavel_selecionada == 'Etnia':
    st.subheader(f"Gráfico de Setores de {variavel_selecionada}")
    fig = px.pie(df, values="Contagem", names=variavel_selecionada)
    st.plotly_chart(fig)
    
    st.write(etnia1)
    st.write(etnia2)

elif variavel_selecionada == 'Experiência':
    
    # Calcular a ordem das categorias de "Experiência"
    ordem_experiencia = df['Experiência'].value_counts().index.tolist()

    # Gráfico: Distribuição de Experiência
    st.subheader('Distribuição de Experiência')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Gráfico de barras: Distribuição de Experiência
    sns.countplot(data=df, x='Experiência', order=ordem_experiencia, ax=ax, color=cor)

    # Calcular e exibir a porcentagem para "Experiência"
    total_experiencia = len(df)
    for p in ax.patches:
        height = p.get_height()
        percentage = (height / total_experiencia) * 100
        ax.text(
            p.get_x() + p.get_width() / 2, height + 1, f'{percentage:.1f}%', 
            ha='center', va='bottom', fontsize=10, color='black'
        )

    # Ajustes no gráfico
    ax.set_title('Distribuição de Experiência', fontsize=16)
    ax.set_xlabel('Experiência', fontsize=12)
    ax.set_ylabel('Contagem', fontsize=12)
    ax.tick_params(axis='x', rotation=45)

    # Exibição do gráfico no Streamlit
    st.pyplot(fig)
    st.write(experiencia1)
    st.write(experiencia2)
    st.write(experiencia3)

elif variavel_selecionada == 'Região':
    tabela_migracao = pd.crosstab(df_migracao['Região de Origem'], df_migracao['Região Atual'])

# Exibir o heatmap da tabela de migração
    opcao_selecao = st.radio('Escolha a versão para visualização:', 
                         ('Contagem', 'Proporção'))

# Calcular as tabelas e a versão normalizada
    tabela_migracao = pd.crosstab(df_migracao['Região de Origem'], df_migracao['Região Atual'])
    tabela_migracao_proporcional = tabela_migracao.div(tabela_migracao.sum(axis=1), axis=0)

# Condicional para escolher qual versão mostrar
    if opcao_selecao == 'Contagem':
        tabela_exibicao = tabela_migracao
        titulo_grafico = 'Região de Origem vs Região Atual (Contagem)'
        fmt = "d"  # Formato de contagem
    else:
        tabela_exibicao = tabela_migracao_proporcional
        titulo_grafico = 'Região de Origem vs Região Atual (Proporção)'
        fmt = ".2f"  # Formato normalizado com 2 casas decimais

    st.subheader(f'Heatmap: {titulo_grafico}')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(tabela_exibicao, annot=True, cmap=corm, fmt=fmt, ax=ax)
    plt.title(titulo_grafico, fontsize=16)
    plt.xlabel('Região Atual', fontsize=12)
    plt.ylabel('Região de Origem', fontsize=12)
    st.pyplot(fig)

    #st.subheader('Tabela de Migração entre Regiões')
    #st.write(tabela_migracao)
    st.write(regiao1)
    st.write(regiao2)
    st.write(regiao3)



else:
    st.write("Escolha uma variável válida.")

st.markdown("---")

###############Analise Bivariada##########################

st.markdown("""
### Análises Bivariada 🌐

Nesta seção, você poderá visualizar 
gráficos que propomos para analisar a 
relação entre duas variáveis da base. 

Divirta-se ✨

""")


###############Interpretação dos Gráificos##########################

idade1 = ""

etnia1 = ""

gênero1 = ""

faixasalarial1 = ""

escolaridade1 = ""

nível1 = ""

cargo1 = "Devido a similaridade entre algumas profissões, ou por conveniência devido à baixa frequência de observações,agrupamos as profissões de sumarizamos seus originais valores na tabela a baixo"
cargo2 = ""

experiência1 = ""

###############Gráificos##########################

variavel_selecionada = st.selectbox('Escolha um cruzamento de variáveis para análise:',
                                    sorted(['Etnia X Idade', 'Etnia X Faixa Salarial', 'Faixa Salarial X Idade','Experiência X Faixa Salarial', #'Cargo X Nível', 'Cargo X Nível X Salário'
                                            ]))


if variavel_selecionada == 'Etnia X Idade':
    
    # Calcular a média das idades por Etnia
    Idades_Etnia = df.groupby('Etnia')['Idade'].mean().sort_values(ascending=True).index

    # Criar o gráfico Boxplot
    fig = px.box(df, x="Etnia", y="Idade",
                 labels={"Etnia": "Etnia", "Idade": "Idades"},
                 title="Boxplot das Idades por Etnia",
                 category_orders={"Etnia": Idades_Etnia})

    fig.update_traces(marker=dict(color=cor))

    fig.update_layout(title_x=0.5)

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)

elif variavel_selecionada == 'Etnia X Faixa Salarial':

    faixas_salariais = {
        "Menos de R$ 1.000/mês": 500,
        "de R$ 1.001/mês a R$ 2.000/mês": 1500,
        "de R$ 2.001/mês a R$ 3.000/mês": 2500,
        "de R$ 3.001/mês a R$ 4.000/mês": 3500,
        "de R$ 4.001/mês a R$ 6.000/mês": 5000,
        "de R$ 6.001/mês a R$ 8.000/mês": 7000,
        "de R$ 8.001/mês a R$ 12.000/mês": 10000,
        "de R$ 12.001/mês a R$ 16.000/mês": 14000,
        "de R$ 16.001/mês a R$ 20.000/mês": 18000,
        "de R$ 20.001/mês a R$ 25.000/mês": 22500,
        "de R$ 25.001/mês a R$ 30.000/mês": 27500,
        "de R$ 30.001/mês a R$ 40.000/mês": 35000,
        "Acima de R$ 40.001/mês": 45000
    }

    df['Faixa Salarial Numérica'] = df['Faixa Salarial'].map(faixas_salariais)

    # Calcular a média dos salários por Etnia
    salario_etnia = df.groupby('Etnia')['Faixa Salarial Numérica'].mean().sort_values(ascending=True).index

    # Criar o gráfico Boxplot para Salários X Etnia
    fig = px.box(df, x="Etnia", y="Faixa Salarial Numérica",
                 labels={"Etnia": "Etnia", "Faixa Salarial Numérica": "Faixa Salarial"},
                 title="Boxplot da Faixa Salarial Médios por Etnia",
                 category_orders={"Etnia": salario_etnia})

    fig.update_traces(marker=dict(color=cor))

    fig.update_layout(title_x=0.5)

    st.plotly_chart(fig)

elif variavel_selecionada == 'Faixa Salarial X Idade':
    # Criar o gráfico Boxplot de Idades por Faixa Salarial, com a ordenação por 'salarios'
    fig = px.box(df.sort_values(by='Faixa Salarial'), x='Faixa Salarial', y="Idade",
                 labels={'Faixa salarial': "Faixa Salarial", "Idade": "Idade"},
                 title="Boxplot das Idades por Faixa Salarial", color="Faixa Salarial")

    # Alterar a cor para uma cor específica
    fig.update_traces(marker=dict(color=cor))  # cor deve ser um valor válido como 'red', 'blue', ou código hexadecimal como '#FF5733'

    # Ajustar o layout do gráfico
    fig.update_layout(title_x=0.5)

    # Ajustar a rotação dos rótulos do eixo X
    fig.update_xaxes(tickangle=90)

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)


elif variavel_selecionada == 'Experiência X Faixa Salarial':
    
    ordem_faixas = [
    "Menos de R$ 1.000/mês",
    "de R$ 1.001/mês a R$ 2.000/mês",
    "de R$ 2.001/mês a R$ 3.000/mês",
    "de R$ 3.001/mês a R$ 4.000/mês",
    "de R$ 4.001/mês a R$ 6.000/mês",
    "de R$ 6.001/mês a R$ 8.000/mês",
    "de R$ 8.001/mês a R$ 12.000/mês",
    "de R$ 12.001/mês a R$ 16.000/mês",
    "de R$ 16.001/mês a R$ 20.000/mês",
    "de R$ 20.001/mês a R$ 25.000/mês",
    "de R$ 25.001/mês a R$ 30.000/mês",
    "de R$ 30.001/mês a R$ 40.000/mês",
    "Acima de R$ 40.001/mês"
    ]
    
    ordem_exp = [
    "Sem experiência",
    "Menos de 1 ano",
    "de 1 a 2 anos",
    "de 3 a 4 anos",
    "de 4 a 6 anos",
    "de 7 a 10 anos",
    "Mais de 10 anos"
    ]
    # Adicionar um radio button para o usuário escolher entre "Contagem" ou "Normalizada"
    opcao_selecao = st.radio('Escolha a versão para visualização:', 
                             ('Contagem', 'Normalizada'))

# Definir a tabela a ser exibida com base na seleção
    tabela_exp_faixa = pd.crosstab(df['Faixa Salarial'], df['Experiência'])
    tabela_exp_faixa = tabela_exp_faixa.reindex(index=ordem_faixas, columns=ordem_exp, fill_value=0)

# Calcular a versão normalizada
    tabela_exp_faixa_p = tabela_exp_faixa.div(tabela_exp_faixa.sum(axis=1), axis=0)

# Condicional para escolher qual versão mostrar
    if opcao_selecao == 'Contagem':
        tabela_exibicao = tabela_exp_faixa
        titulo_grafico = 'Experiência vs Faixa Salarial (Contagem)'
        fmt = "d"  # Formato de contagem
    else:
        tabela_exibicao = tabela_exp_faixa_p
        titulo_grafico = 'Experiência vs Faixa Salarial (Normalizado)'
        fmt = ".3f"  # Formato normalizado com 3 casas decimais

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(tabela_exibicao, annot=True, cmap=corm, fmt=fmt, ax=ax)
    plt.title(titulo_grafico, fontsize=16)
    plt.xlabel('Experiência', fontsize=12)
    plt.ylabel('Faixa Salarial', fontsize=12)
    st.pyplot(fig)

elif variavel_selecionada == 'Cargo X Nível':
    
    def faixa_para_valor(faixa):
        try:
            # Extrair os valores mínimo e máximo de cada faixa
            valores = faixa.split(" a ")
            min_valor = int(valores[0].replace("de R$", "").replace("mês", "").replace(",", "").strip())
            max_valor = int(valores[1].replace("R$", "").replace("mês", "").replace(",", "").strip())
            
            # Retornar a média da faixa salarial
            return (min_valor + max_valor) / 2
        except Exception as e:
            return None  # Caso o formato não seja esperado, retorna None

    # Aplicar a função para converter 'Faixa Salarial' para valores numéricos
    df['Faixa Salarial Valor'] = df['Faixa Salarial'].apply(faixa_para_valor)

    nivel_agrupado = df.groupby(["Cargo", "Nível"], as_index=False)["Faixa Salarial Valor"].mean()

    # Ordenar os cargos com base na média dos salários
    salarios_cargo = df.groupby('Cargo')['Faixa Salarial Valor'].mean().sort_values(ascending=True).index

    # Criar o gráfico de barras
    fig = px.bar(nivel_agrupado, x="Cargo", y="Faixa Salarial Valor",
                 labels={"Cargo": "Cargos", "Faixa Salarial Valor": "Faixa Salarial", "Nível": "Nível"},
                 title="Salários Médios por Cargos e Nível de Senioridade",
                 color="Nível", barmode="group",
                 category_orders={'Cargo': salarios_cargo})

    # Ajustar o layout do gráfico
    fig.update_layout(title_x=0.5)

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)
   
    
   
elif variavel_selecionada == 'Cargo X Nível X Salário':
    
    nivel_agrupado = df.groupby(["Cargo", "Nível"], as_index=False)["Faixa Salarial"].mean()


    salarios_cargo = df.groupby('Cargo')['Faixa Salarial'].mean().sort_values(ascending=True).index


    fig = px.bar(nivel_agrupado, x="Cargo", y="Faixa Salarial",
             labels={"Cargo": "Cargos", "Faixa Salarial": "Salários", "Nível": "Nível"},
             title="Faixa Salarial Média por Cargos e Nível de Senioridade",
             color="Nível", barmode="group",
             category_orders={'Cargo': salarios_cargo})

    fig.update_layout(title_x=0.5)

    st.plotly_chart(fig)
    
    nivel_agrupado = df.groupby(["Cargo", "Nível"], as_index=False)["salarios"].mean()


    salarios_cargo = df.groupby('Cargo')['salarios'].mean().sort_values(ascending=True).index


    fig = px.bar(nivel_agrupado, x="Cargo", y="salarios",
             labels={"Cargo": "Cargos", "salarios": "Salários", "Nível": "Nível"},
             title="Salários Médios por Cargos e Nível de Senioridade",
             color="Nível", barmode="group",
             category_orders={'Cargo': salarios_cargo})

    fig.update_layout(title_x=0.5)

    st.plotly_chart(fig)