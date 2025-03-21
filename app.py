import streamlit as st
import pandas as pd
import urllib.parse

# 🔹 Configuração da página
st.set_page_config(page_title="Catálogo de Peças JDEMITO", layout="wide")

# URL base do repositório GitHub onde as imagens estão armazenadas
GITHUB_REPO_URL = "https://raw.githubusercontent.com/ArkaltRefrigeracao/app-jdemito/main/"

# 🔹 Adicionar fundo azul claro via CSS (Imagem da internet)
st.markdown("""
    <style>
    body {
        background-image: url('https://www.colorhexa.com/d6e6f2.png');
        background-size: cover;
    }
    .stApp {
        background-color: rgba(214, 230, 242, 0.85); /* Azul claro com transparência */
        padding: 20px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Função para carregar os dados da planilha
@st.cache_data(ttl=60)
def load_data():
    df_placas = pd.read_excel("TESTE 222.xlsx", sheet_name="PLACAS")
    df_pecas = pd.read_excel("TESTE 222.xlsx", sheet_name="PEÇAS22")
    return df_placas, df_pecas

# Criar um botão para atualizar manualmente os dados
if st.button("🔄 Atualizar Dados"):
    st.cache_data.clear()
    st.rerun()

# Carregar os dados da planilha
df_placas, df_pecas = load_data()

# Criar um layout flexível com colunas
col1, col2, col3 = st.columns([1, 3, 1])  

with col2:
    st.markdown("""
        <h1 style='text-align: center; color: #003366;'>
            CATÁLOGO DE PEÇAS
        </h1>
    """, unsafe_allow_html=True)

    st.markdown("<h4 style='text-align: center; color: #FFC300;'>Grupo J. Demito</h4>", unsafe_allow_html=True)  # Amarelo dourado

# Padronização do estilo dos títulos
titulo_azul_escuro = "font-size:20px; font-weight:bold; color:#003366;"  # Azul escuro
titulo_azul_claro = "font-size:20px; font-weight:bold; color:#0055A4;"  # Azul mais claro
titulo_cinza_claro = "font-size:20px; font-weight:bold; color:#666666;"  # Cinza mais claro

# Seleção do tipo de veículo (com azul escuro)
st.markdown(f"<p style='{titulo_azul_escuro}'>🚛 Escolha o tipo de veículo:</p>", unsafe_allow_html=True)
tipo_veiculo = st.selectbox("", df_placas["TIPO DE VEÍCULO"].unique())

# Seleção da placa (com cinza mais claro)
st.markdown(f"<p style='{titulo_cinza_claro}'>🚗 Escolha a placa:</p>", unsafe_allow_html=True)
placas_filtradas = df_placas[df_placas["TIPO DE VEÍCULO"] == tipo_veiculo]
placa = st.selectbox("", placas_filtradas["PLACA"])

# Exibir peças disponíveis (com azul mais claro)
st.markdown(f"<p style='{titulo_azul_claro}'>🛠️ Peças disponíveis:</p>", unsafe_allow_html=True)
pecas_disponiveis = df_pecas[df_pecas["PLACA"] == placa][["PEÇA", "CÓDIGO"]].values.tolist()

# Exibição das peças com caixas de seleção e imagens
pecas_selecionadas = []

for idx, (peca, codigo) in enumerate(pecas_disponiveis):
    unique_key = f"checkbox_{idx}"
    selecionado = st.checkbox(f"{peca} (Código: {codigo})", key=unique_key)
    
    if selecionado:
        pecas_selecionadas.append((peca, codigo))
        imagem_url = f"{GITHUB_REPO_URL}{codigo}.jpg"  # URL da imagem da peça
        st.image(imagem_url, width=180)  # 🔹 Tamanho da imagem 180px

# Função para gerar a mensagem formatada
def gerar_mensagem(tipo_veiculo, placa, pecas_selecionadas):
    mensagem = f"""
    Olá, gostaria de um orçamento:
    
    🚗 Veículo: {tipo_veiculo}
    🔢 Placa: {placa}
    
    🛠️ Peças solicitadas:
    """
    for peca, codigo in pecas_selecionadas:
        mensagem += f"- {peca} (Código: {codigo})\n"
    return mensagem.strip()

# Botões para solicitar orçamento
numero_whatsapp1 = "556392930759"
numero_whatsapp2 = "556392099424"

if pecas_selecionadas:
    mensagem_formatada = gerar_mensagem(tipo_veiculo, placa, pecas_selecionadas)
    link_whatsapp1 = f"https://api.whatsapp.com/send?phone={numero_whatsapp1}&text={urllib.parse.quote(mensagem_formatada)}"
    link_whatsapp2 = f"https://api.whatsapp.com/send?phone={numero_whatsapp2}&text={urllib.parse.quote(mensagem_formatada)}"
    
    st.markdown(f'<a href="{link_whatsapp1}" style="display: block; padding: 10px; text-align: center; background-color: #4A90E2; color: white; text-decoration: none; border-radius: 5px;">📞 Solicitar Orçamento (Vendedor Gustavo)</a>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<a href="{link_whatsapp2}" style="display: block; padding: 10px; text-align: center; background-color: #4A90E2; color: white; text-decoration: none; border-radius: 5px;">📞 Solicitar Orçamento (Vendedor José)</a>', unsafe_allow_html=True)
