import streamlit as st
import pandas as pd
import pydeck as pdk
from geodata import GEO_SPO 

# 1. CONFIGURAÇÃO E IDENTIDADE VISUAL (PRETO, AMARELO, VERMELHO)
st.set_page_config(page_title="Beta II - Calculadora do Trecho", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    
    /* VISIBILIDADE DOS TÍTULOS E LABELS */
    label, p, span, .stSelectbox label { 
        color: #FFCC00 !important; 
        font-weight: 800 !important; 
        text-transform: uppercase !important;
        font-size: 1rem !important;
    }

    .chamada-alerta { 
        background-color: #E63946; color: white; text-align: center; 
        padding: 15px; font-weight: 900; border: 4px solid #FFCC00; 
        margin-bottom: 10px; text-transform: uppercase; font-size: 1.6rem;
    }
    
    .titulo-pergunta { 
        color: #FFCC00 !important; font-family: 'Arial Black', sans-serif; 
        font-size: 1.4rem !important; text-align: center; 
        text-transform: uppercase; margin-bottom: 30px; line-height: 1.2;
    }

    .secao-titulo { 
        color: #FFCC00 !important; font-size: 1.2rem !important; font-weight: 800; 
        text-transform: uppercase; margin-top: 30px; border-bottom: 2px solid #FFCC00; padding-bottom: 5px; 
    }

    /* AJUSTE DOS INPUTS (MAIORES PARA UX) */
    .stNumberInput input {
        background-color: #111 !important;
        color: #FFFFFF !important;
        font-size: 1.2rem !important;
        border: 1px solid #FFCC00 !important;
    }

    .sintese-box { 
        background-color: #111; border: 2px solid #FFCC00; 
        padding: 20px; margin-top: 20px; color: #FFFFFF; 
        font-family: 'Courier New', monospace; line-height: 1.6; 
    }
    .destaque-amarelo { color: #FFCC00; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

lista_geo = sorted(list(GEO_SPO.keys()))

# 2. CABEÇALHO COM AS CHAMADAS SOLICITADAS
st.markdown('<div class="chamada-alerta">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="titulo-pergunta">Quanto de tempo e de dinheiro são consumidos no seu deslocamento diário?</div>', unsafe_allow_html=True)

with st.form("beta_ii_v8"):
    c_geo1, c_geo2 = st.columns(2)
    with c_geo1: moradia = st.selectbox("🏠 ORIGEM (MORADIA):", lista_geo, index=0)
    with c_geo2: trabalho = st.selectbox("💼 DESTINO (TRABALHO):", lista_geo, index=1)
    
    st.markdown('<div class="secao-titulo">💵 RENDIMENTOS E SOBREVIVÊNCIA</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: sal_bruto = st.number_input("SALÁRIO BRUTO MENSAL (R$):", min_value=1.0, value=3000.0, step=100.0)
    with c2: custo_vida = st.number_input("CUSTO DE VIDA FIXO (R$):", min_value=0.0, value=1500.0, step=50.0)
    
    st.markdown('<div class="secao-titulo">🚌 CUSTOS NO TRECHO (ÔNIBUS/METRÔ/TREM/APP/CARRO)</div>', unsafe_allow_html=True)
    g1, g2 = st.columns(2)
    with g1: p_diario = st.number_input("GASTO DIÁRIO TOTAL (IDA+VOLTA):", min_value=0.0, value=8.80, step=0.5)
    with g2: dias_mes = st.number_input("DIAS DE DESLOCAMENTO/MÊS:", 1, 31, 22)
    
    st.markdown('<div class="secao-titulo">⏱️ TEMPO DE EXPROPRIAÇÃO</div>', unsafe_allow_html=True)
    h_trecho_dia = st.slider("TOTAL DE HORAS NO TRECHO POR DIA (IDA+VOLTA):", 0.5, 12.0, 3.0, step=0.5)
    
    btn = st.form_submit
