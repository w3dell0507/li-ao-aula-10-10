import streamlit as st
from PIL import Image, ImageStat
import numpy as np

st.set_page_config(page_title="Simulador de Detecção de Objetos", layout="centered")

st.title("🔍 Simulação de Detecção de Objetos por Regras")
st.write("Este sistema utiliza regras heurísticas básicas (como cor predominante e brilho) para simular a detecção de elementos em uma imagem.")

uploaded_file = st.file_uploader("Envie uma imagem para análise", type=["jpg", "jpeg", "png"])

def analisar_imagem(image):
    # Converte imagem para RGB
    img_rgb = image.convert('RGB')
    stat = ImageStat.Stat(img_rgb)
    
    # Médias dos canais de cor R, G, B
    r, g, b = stat.mean
    
    # Converte para array numpy para calcular brilho médio
    img_np = np.array(img_rgb)
    brilho_medio = np.mean(img_np)
    
    deteccoes = []
    
    # Regra 1: Detecção de Céu / Paisagem (Predominância de Azul)
    if b > r and b > g:
        deteccoes.append("🌤️ Céu / Ambiente Aquático (Predominância de tons azuis)")
        
    # Regra 2: Detecção de Vegetação / Natureza (Predominância de Verde)
    if g > r and g > b:
        deteccoes.append("🌿 Vegetação / Natureza (Predominância de tons verdes)")
        
    # Regra 3: Detecção de Objeto Quente / Humano (Predominância de Vermelho/Tons quentes)
    if r > g and r > b:
        deteccoes.append("🚗/👤 Objeto em Destaque / Veículo / Tons Quentes")
        
    # Regra 4: Análise de Iluminação
    if brilho_medio > 180:
        deteccoes.append("☀️ Ambiente Externo / Iluminado")
    elif brilho_medio < 70:
        deteccoes.append("🌙 Ambiente Noturno / Sombra Densa")
        
    if not deteccoes:
        deteccoes.append("📦 Objeto Indefinido / Padrão Geral")
        
    return deteccoes, (r, g, b), brilho_medio

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagem Carregada", use_column_width=True)
    
    with st.spinner("Analisando padrões da imagem..."):
        deteccoes, (r, g, b), brilho = analisar_imagem(image)
        
    st.subheader("📊 Resultados da Detecção:")
    for det in deteccoes:
        st.success(f"- {det}")
        
    with st.expander("Ver dados técnicos da análise"):
        st.write(f"**Média Canal Vermelho (R):** {r:.2f}")
        st.write(f"**Média Canal Verde (G):** {g:.2f}")
        st.write(f"**Média Canal Azul (B):** {b:.2f}")
        st.write(f"**Brilho Médio:** {brilho:.2f}")