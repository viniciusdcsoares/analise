template_graficos = st.sidebar.selectbox(
    "Escolha o tema dos gráficos:",
   ["Tema Claro", "Tema Escuro"])

template_pagina = st.sidebar.selectbox(
    "Escolha o tema da página:",
   ["Tema Claro", "Tema Escuro"])

if template_graficos == "Tema Escuro":
    template_graph = "black"
    template_plotly = "plotly_white"
else:
    template_graph = "white"
    template_plotly = "plotly_dark"  