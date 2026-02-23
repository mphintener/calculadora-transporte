import streamlit as st
import pandas as pd
from geodata import GEO_SPO 

# 1. IDENTIDADE VISUAL (ALTO CONTRASTE)
st.set_page_config(page_title="Beta II - Calculadora do Trecho", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    
    label, .stSelectbox label, .stNumberInput label { 
        color: #FFCC00 !important; font-weight: 800 !important; 
        text-transform: uppercase !important; font-size: 1.1rem !important;
    }

    .chamada-alerta { 
        background-color: #E63946; color: white; text-align: center; 
        padding: 15px; font-weight: 900; border: 4px solid #FFCC00; 
        margin-bottom: 10px; text-transform: uppercase; font-size: 1.5rem;
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

    .stNumberInput input { background-color: #111 !important; color: #FFFFFF !important; font-size: 1.2rem !important; border: 1px solid #FFCC00 !important; }

    .sintese-box { 
        background-color: #111; border: 2px solid #FFCC00; 
        padding: 20px; margin-top: 10px; color: #FFFFFF; 
        font-family: 'Courier New', monospace; font-size: 1.1rem; line-height: 1.5;
    }
    
    .expro-destaque { color: #E63946; font-weight: 900; font-size: 1.4rem; }
    .valor-amarelo { color: #FFCC00; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

lista_geo = sorted(list(GEO_SPO.keys()))

st.markdown('<div class="chamada-alerta">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="titulo-pergunta">Quanto de tempo e de dinheiro são consumidos no seu deslocamento diário?</div>', unsafe_allow_html=True)

with st.form("form_beta_ii_final"):
    st.markdown('<div class="secao-titulo">🏠 ORIGEM E DESTINO</div>', unsafe_allow_html=True)
    c_geo1, c_geo2 = st.columns(2)
    with c_geo1: moradia = st.selectbox("MORO EM:", lista_geo, index=0)
    with c_geo2: trabalho = st.selectbox("TRABALHO EM:", lista_geo, index=1)
    
    st.markdown('<div class="secao-titulo">💵 RENDIMENTOS E SOBREVIVÊNCIA</div>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    with r1: sal_bruto = st.number_input("SALÁRIO BRUTO (R$):", min_value=1.0, value=3000.0)
    with r2: custo_v = st.number_input("CUSTO DE VIDA FIXO (R$):", min_value=0.0, value=1500.0)
    
    st.markdown('<div class="secao-titulo">🚌 CUSTOS NO TRECHO (DIÁRIO)</div>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1: p_pub = st.number_input("🚆 PÚBLICO (R$)", value=8.80)
    with g2: p_app = st.number_input("📱 APP (R$)", value=0.0)
    with g3: p_car = st.number_input("🚗 CARRO (R$)", value=0.0)
    
    dias_m = st.number_input("DIAS DE TRECHO NO MÊS:", 1, 31, 22)
    h_dia = st.slider("HORAS NO TRECHO POR DIA (TOTAL):", 0.5, 12.0, 3.0, step=0.5)
    
    submit = st.form_submit_button("ANALISAR EXPROPRIAÇÃO")

if submit:
    # LÓGICA TÉCNICA
    h_pagas = 176
    custo_transp_total = (p_pub + p_app + p_car) * dias_m
    h_trecho_total = h_dia * dias_m
    
    v_hora_nom = sal_bruto / h_pagas
    # O rendimento real agora flutua baseado no tempo não pago e custos
    v_hora_real = (sal_bruto - custo_transp_total) / (h_pagas + h_trecho_total)
    
    perda_p = (1 - (v_hora_real / v_hora_nom)) * 100
    sobra = sal_bruto - custo_transp_total - custo_v

    # VETOR VISUAL (SUBSTITUTO DO MAPA)
    st.markdown('<div class="secao-titulo">🗺️ VETOR DE FLUXO PENDULAR</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: space-around; background: #111; padding: 20px; border: 1px solid #333;">
            <div style="color: #FFCC00; font-weight: bold;">🏠 {moradia}</div>
            <div style="color: #E63946; font-size: 2rem;">――――▶</div>
            <div style="color: #FFCC00; font-weight: bold;">💼 {trabalho}</div>
        </div>
    """, unsafe_allow_html=True)

    # SÍNTESE DA EXPROPRIAÇÃO (COMPACTA)
    st.markdown('<div class="secao-titulo">📝 SÍNTESE DA EXPROPRIAÇÃO</div>', unsafe_allow_html=True)
    sintese_txt = (f"Ao se deslocar entre {moradia} e {trabalho}, você gasta R$ {custo_transp_total:.2f} mensais e "
                   f"dedica {h_trecho_total:.1f} HORAS NÃO REMUNERADAS ao sistema. O seu rendimento real cai para R$ {v_hora_real:.2f}/h.")
    st.markdown(f'<div class="sintese-box">{sintese_txt}</div>', unsafe_allow_html=True)

    # MÉTRICAS CONSOLIDADAS
    st.markdown('<div class="secao-titulo">🔬 MÉTRICAS CONSOLIDADAS</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="sintese-box">
            • <span class="expro-destaque">HORAS DE TRABALHO NÃO PAGAS:</span> {h_trecho_total:.1f}h/mês<br>
            • <span class="valor-amarelo">VALOR DA HORA (NOMINAL):</span> R$ {v_hora_nom:.2f}<br>
            • <span class="expro-destaque">VALOR DA HORA (REAL):</span> R$ {v_hora_real:.2f}<br>
            • <span class="valor-amarelo">SALÁRIO REAL CONFISCADO:</span> {perda_p:.1f}%<br>
            • <span class="valor-amarelo">RENDIMENTO RESIDUAL (SOBRA):</span> R$ {sobra:.2f}
        </div>
    """, unsafe_allow_html=True)
