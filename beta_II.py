import streamlit as st
import pandas as pd
from geodata import GEO_SPO 

# 1. ESTILO TERMINAL URBANO REFINADO (ALTO CONTRASTE)
st.set_page_config(page_title="Beta II - Calculadora do Trecho", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    
    /* LABELS EM AMARELO 99 */
    label, .stSelectbox label, .stNumberInput label { 
        color: #FFCC00 !important; 
        font-weight: 800 !important; 
        text-transform: uppercase !important;
        font-size: 1.1rem !important;
    }

    .chamada-alerta { 
        background-color: #E63946; color: white; text-align: center; 
        padding: 15px; font-weight: 900; border: 4px solid #FFCC00; 
        margin-bottom: 10px; text-transform: uppercase; font-size: 1.6rem;
    }
    
    .titulo-pergunta { 
        color: #FFCC00 !important; font-family: 'Arial Black', sans-serif; 
        font-size: 1.4rem !important; text-align: center; 
        text-transform: uppercase; margin-bottom: 30px;
    }

    .secao-titulo { 
        color: #FFCC00 !important; font-size: 1.2rem !important; font-weight: 800; 
        text-transform: uppercase; margin-top: 30px; border-bottom: 2px solid #FFCC00; padding-bottom: 5px; 
    }

    /* QUADROS DE RESULTADO */
    .sintese-box { 
        background-color: #111; border: 2px solid #FFCC00; 
        padding: 20px; margin-top: 10px; color: #FFFFFF; 
        font-family: 'Courier New', monospace; font-size: 1.1rem; line-height: 1.5;
    }
    
    /* VETOR DE FLUXO (SUBSTITUTO DO MAPA) */
    .vetor-fluxo {
        display: flex; align-items: center; justify-content: space-around;
        background: #111; padding: 30px; border-radius: 10px; border: 1px solid #333;
        margin-top: 20px;
    }
    .localidade { color: #FFCC00; font-family: 'Arial Black'; font-size: 1.2rem; text-align: center; }
    .seta-fluxo { color: #E63946; font-size: 2.5rem; font-weight: bold; }
    
    .destaque-valor { color: #FFCC00; font-weight: bold; }
    .destaque-perda { color: #E63946; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

lista_geo = sorted(list(GEO_SPO.keys()))

st.markdown('<div class="chamada-alerta">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="titulo-pergunta">Quanto de tempo e de dinheiro são consumidos no seu deslocamento diário?</div>', unsafe_allow_html=True)

with st.form("beta_ii_v13"):
    st.markdown('<div class="secao-titulo">🏠 GEOGRAFIA DO TRECHO</div>', unsafe_allow_html=True)
    c_geo1, c_geo2 = st.columns(2)
    with c_geo1: moradia = st.selectbox("MORO EM:", lista_geo, index=0)
    with c_geo2: trabalho = st.selectbox("TRABALHO EM:", lista_geo, index=1)
    
    st.markdown('<div class="secao-titulo">💵 RENDIMENTOS E SOBREVIVÊNCIA</div>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    with r1: sal_bruto = st.number_input("SALÁRIO BRUTO (R$):", min_value=1.0, value=3000.0)
    with r2: custo_vida = st.number_input("CUSTO DE VIDA FIXO (R$):", min_value=0.0, value=1500.0, help="Gasto opcional com aluguel e contas. Não afeta o valor da hora.")
    
    st.markdown('<div class="secao-titulo">🚌 CUSTOS NO TRECHO (ÔNIBUS/METRÔ/APP/CARRO)</div>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1: p_pub = st.number_input("🚆 PÚBLICO (R$)", min_value=0.0, value=8.80)
    with g2: p_app = st.number_input("📱 APP/TÁXI (R$)", min_value=0.0)
    with g3: p_car = st.number_input("🚗 CARRO/MOTO (R$)", min_value=0.0)
    
    st.write("")
    d3, d4 = st.columns(2)
    with d3: dias_mes = st.number_input("DIAS NO TRECHO / MÊS:", 1, 31, 22)
    with d4: h_trecho = st.slider("HORAS NO TRECHO / DIA:", 0.5, 12.0, 3.0, step=0.5)
    
    btn = st.form_submit_button("PROCESSAR IMPACTO REAL")

if btn:
    # LÓGICA TÉCNICA (CONFORME DIRETRIZES DO USUÁRIO)
    h_pagas_mes = 176
    custo_transp_mes = (p_pub + p_app + p_car) * dias_mes
    h
