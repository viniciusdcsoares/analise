import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Aplicativo",
    page_icon="🤓",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Sidebar para seleção de tema pelo usuário
tema_app = st.sidebar.selectbox("Escolha o tema do aplicativo:", ["Tema Claro", "Tema Escuro"])

# Tema das páginas baseados na seleção do usuário
if tema_app == "Tema Escuro":
    sidebar_bg_color = "#333333"
    sidebar_text_color = "white"
    main_bg_color = "#000000"
    main_text_color = "white"
    input_bg_color = "#222222"
    input_text_color = "white"
    border_color = "#555555"
    dropdown_bg_color = "#222222"
    dropdown_text_color = "white"
else:
    sidebar_bg_color = "#f0f0f0"
    sidebar_text_color = "black"
    main_bg_color = "#ffffff"
    main_text_color = "black"
    input_bg_color = "#ffffff"  # Branco no tema claro
    input_text_color = "black"  # Texto preto
    border_color = "#cccccc"
    dropdown_bg_color = "#ffffff"  # Dropdown branco no tema claro
    dropdown_text_color = "black"
    


# Tema dos gráficos baseados na seleção do usuário
if tema_app == "Tema Escuro":
    st.session_state.template_graph = "black"
    st.session_state.template_plotly = "plotly_white"
else:
    st.session_state.template_graph = "white"
    st.session_state.template_plotly = "plotly_dark"

# default
if "template_graph" not in st.session_state:
    st.session_state.template_graph = "white"  
if "template_plotly" not in st.session_state:
    st.session_state.template_plotly = "plotly_dark"

# Apply global CSS for styling
st.markdown(
    f"""
    <style>
    /* Fundo e cor do texto principal */
    html, body, .stApp {{
        background-color: {main_bg_color} !important;
        color: {main_text_color} !important;
    }}
    
    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg_color} !important;
        color: {sidebar_text_color} !important;
    }}

    /* Estilização geral do texto */
    h1, h2, h3, h4, h5, h6, p, div, span, label {{
        color: {main_text_color} !important;
    }}

    /* Inputs, selects e textareas */
    input, select, textarea {{
        background-color: {input_bg_color} !important;
        color: {input_text_color} !important;
        border-radius: 5px !important;
        border: 1px solid {border_color} !important;
        padding: 6px !important;
        box-shadow: none !important;  /* Remove qualquer espaço extra */
    }}

    /* Ajustando dropdowns (caixas abertas) */
    div[data-baseweb="popover"] {{
        background-color: {dropdown_bg_color} !important;
        color: {dropdown_text_color} !important;
        border: 1px solid {border_color} !important;
    }}

    /* Itens dentro dos selects */
    div[data-baseweb="option"] {{
        background-color: {dropdown_bg_color} !important;
        color: {dropdown_text_color} !important;
    }}

    /* Remove espaço extra nas caixas de seleção */
    div[data-testid="stSelectbox"] div {{
        background-color: {input_bg_color} !important;
        color: {input_text_color} !important;
        border: none !important;
    }}

    /* Evita edição manual no selectbox */
    div[data-baseweb="select"] input {{
        pointer-events: none !important;
    }}

    /* Forçando cor do texto dentro dos inputs */
    input::placeholder, textarea::placeholder {{
        color: {input_text_color} !important;
        opacity: 0.7 !important;
    }}

    /* Ajustando botões */
    button {{
        background-color: {input_bg_color} !important;
        color: {input_text_color} !important;
        border-radius: 5px !important;
        border: 1px solid {border_color} !important;
    }}

    /* Remove o fundo branco ao passar o mouse nos selects */
    div[data-baseweb="select"]:hover {{
        background-color: {input_bg_color} !important;
    }}

    /* Remove qualquer sombra no botão e inputs */
    button, input, select, textarea {{
        box-shadow: none !important;
    }}

    /* Evita que o Streamlit sobrescreva as cores */
    div[class^="st-"], span[class^="st-"], button {{
        color: {main_text_color} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Teste para ver as mudanças
st.title("Teste de Tema")
st.write("Esse é um texto de teste para verificar o tema.")

st.text_input("Digite algo aqui:")
st.selectbox("Escolha uma opção:", ["Opção 1", "Opção 2"])
st.multiselect("Escolha várias opções:", ["A", "B", "C"])
st.button("Botão de teste")

# Definindo as páginas
paginas = {
    "": [
        st.Page("paginas/home.py", title="Página Inicial", icon="🤓", default=True)
    ],
    "Gráficos Univariados 📈": [
        st.Page("paginas/univariadas.py", title="Análise Geral das Variáveis", icon="🤓")
    ],
    "  ": [
        st.Page("paginas/univariadas2.py", title="Salários", icon="💰")
    ],
#    "    ": [
#        st.Page("paginas/bivariadas.py", title="Análise Bivariada", icon="🤓")
#    ],
    "Gráficos Bivariados": [
        st.Page("paginas/bivariadas.py", title="Análise Bivariada", icon="🤓")
    ],
    "   ": [
        st.Page("paginas/bivariadas2.py", title="Análise Bivariada", icon="🤓")
    ],
}
pg = st.navigation(paginas)
pg.run()