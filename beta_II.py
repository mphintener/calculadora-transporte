import streamlit as st
import pandas as pd
from geodata import GEO_SPO 

# 1. ESTILO TERMINAL URBANO (ALTO CONTRASTE)
st.set_page_config(page_title="Beta II - Calculadora do Trecho", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    
    /* LABELS EM AMARELO */
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

    /* INPUTS TOTALMENTE EDITÁVEIS E LIMPOS */
    .stNumberInput div[data-baseweb="input"] { background-color: #111 !important; border: 2px solid #333 !important; }
    .stNumberInput input { color: #FFFFFF !important; font-size: 1.3rem !important; }

    /* QUADROS DE RESULTADO */
    .sintese-box { 
        background-color: #111; border: 2px solid #FFCC00; 
        padding: 20px; margin-top: 10px; color: #FFFFFF; 
        font-family: 'Courier New', monospace; font-size: 1.1rem; line-height: 1.5;
    }
    
    .expro-destaque { color: #E63946; font-weight: 900; border-bottom: 2px solid #E63946; }
    .valor-amarelo { color: #FFCC00; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

lista_geo = sorted(list(GEO_SPO.keys()))

st.markdown('<div class="chamada-alerta">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="titulo-pergunta">Quanto de tempo e de dinheiro são consumidos no seu deslocamento diário?</div>', unsafe_allow_html=True)

with st.form("beta_ii_v14"):
    st.markdown('<h4 style="color:#FFCC00">🏠 GEOGRAFIA DO FLUXO</h4>', unsafe_allow_html=True)
    c_geo1, c_geo2 = st.columns(2)
    with c_geo1: moradia = st.selectbox("ORIGEM (MORADIA):", lista_geo, index=0)
    with c_geo2: trabalho = st.selectbox("DESTINO (TRABALHO):", lista_geo, index=1)
    
    st.markdown('<h4 style="color:#FFCC00">💵 ECONOMIA PESSOAL</h4>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    with r1: sal_bruto = st.number_input("SALÁRIO BRUTO (R$):", min_value=0.0, max_value=100000.0, value=3000.0, step=100.0)
    with r2: custo_vida = st.number_input("CUSTO DE VIDA FIXO (R$):", min_value=0.0, max_value=100000.0, value=1500.0, step=50.0, 
                                         help="Preenchimento opcional: Aluguel, mercado e contas. Este valor não altera o valor da hora técnica, apenas a sobra final.")
    
    st.markdown('<h4 style="color:#FFCC00">🚌 LOGÍSTICA (DIÁRIO)</h4>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1: p_pub = st.number_input("🚆 PÚBLICO", value=8.80)
    with g2: p_app = st.number_input("📱 APP", value=0.0)
    with g3: p_car = st.number_input("🚗 CARRO", value=0.0)
    
    dias_m = st.number_input("DIAS DE TRECHO NO MÊS:", 1, 31, 22)
    h_dia = st.slider("TOTAL DE HORAS NO TRECHO (DIA):", 0.5, 12.0, 3.0, step=0.5)
    
    submit = st.form_submit_button("PROCESSAR DADOS DE EXPROPRIAÇÃO")

if submit:
    # LÓGICA TÉCNICA REFINADA
    h_pagas = 176
    v_hora_nom = sal_bruto / h_pagas
    custo_transp_total = (p_pub + p_app + p_car) * dias_m
    h_trecho_total = h_dia * dias_m
    
    # Rendimento Real considerando o tempo como trabalho não pago
    v_hora_real = (sal_bruto - custo_transp_total) / (h_pagas + h_trecho_total)
    perda_p = (1 - (v_hora_real / v_hora_nom)) * 100
    sobra = sal_bruto - custo_transp_total - custo_vida

    # VETOR DE IMPACTO (ALTERNATIVA AO MAPA)
    st.markdown('<h4 style="color:#FFCC00">🗺️ VETOR DE IMPACTO GEOGRÁFICO</h4>', unsafe_allow_html=True)
    st.markdown(f"""
        <div style="background: #111; padding: 30px; border-radius: 10px; border: 1px solid #E63946; text-align: center;">
            <span style="color:#FFCC00; font-size:1.2rem; font-weight:bold;">🏠 {moradia}</span>
            <span style="color:#E63946; font-size:2rem; margin: 0 20px;">⚡――――――――▶</span>
            <span style="color:#FFCC00; font-size:1.2rem; font-weight:bold;">💼 {trabalho}</span>
            <p style="color:#E63946; margin-top:15px; font-weight:bold; text-transform:uppercase;">
                O deslocamento casa-trabalho-casa é tempo de trabalho não pago.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # SÍNTESE PARA COMUNICAÇÃO PÚBLICA
    st.markdown('<h4 style="color:#FFCC00">📝 SÍNTESE DA EXPROPRIAÇÃO</h4>', unsafe_allow_html=True)
    sintese_txt = (f"MOBILIDADE GSP: O trajeto {moradia}-{trabalho} confisca {perda_p:.1f}% do rendimento real. "
                   f"O valor da hora cai para R$ {v_hora_real:.2f}, resultando em {h_trecho_total:.0f} horas não pagas por mês.")
    st.markdown(f'<div class="sintese-box">{sintese_txt}</div>', unsafe_allow_html=True)

    # MÉTRICAS CONSOLIDADAS
    st.markdown('<h4 style="color:#FFCC00">🔬 RELATÓRIO TÉCNICO</h4>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="sintese-box">
            • <span class="expro-destaque">HORAS DE TRABALHO NÃO PAGAS:</span> {h_trecho_total:.1f}h/mês<br>
            • <span class="valor-amarelo">VALOR DA HORA (NOMINAL):</span> R$ {v_hora_nom:.2f}<br>
            • <span class="expro-destaque">VALOR DA HORA (REAL):</span> R$ {v_hora_real:.2f}<br>
            • <span class="valor-amarelo">SALÁRIO REAL CONFISCADO:</span> {perda_p:.1f}%<br>
            • <span class="valor-amarelo">RENDIMENTO RESIDUAL (SOBRA):</span> R$ {sobra:.2f}
        </div>
    """, unsafe_allow_html=True)
