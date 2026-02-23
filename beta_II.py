import streamlit as st
import pandas as pd
from geodata import GEO_SPO 

# 1. IDENTIDADE VISUAL DE ALTO CONTRASTE
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

    .stNumberInput input { background-color: #111 !important; color: #FFFFFF !important; font-size: 1.2rem !important; border: 1px solid #FFCC00 !important; }

    .sintese-box { 
        background-color: #111; border: 2px solid #FFCC00; 
        padding: 20px; margin-top: 10px; color: #FFFFFF; 
        font-family: 'Courier New', monospace; font-size: 1.1rem; line-height: 1.5;
    }
    
    .expro-destaque { color: #E63946; font-weight: 900; }
    .valor-amarelo { color: #FFCC00; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

lista_geo = sorted(list(GEO_SPO.keys()))

st.markdown('<div class="chamada-alerta">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="titulo-pergunta">Quanto de tempo e de dinheiro são consumidos no seu deslocamento diário?</div>', unsafe_allow_html=True)

with st.form("form_beta_ii_final"):
    st.markdown('<h4 style="color:#FFCC00">🏠 GEOGRAFIA DO TRECHO</h4>', unsafe_allow_html=True)
    c_geo1, c_geo2 = st.columns(2)
    with c_geo1: moradia = st.selectbox("ORIGEM (MORADIA):", lista_geo, index=0)
    with c_geo2: trabalho = st.selectbox("DESTINO (TRABALHO):", lista_geo, index=1)
    
    st.markdown('<h4 style="color:#FFCC00">💵 RENDIMENTOS E SOBREVIVÊNCIA</h4>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    with r1: sal_bruto = st.number_input("SALÁRIO BRUTO (R$):", min_value=0.0, value=3000.0, key="sal_bruto")
    with r2: custo_v = st.number_input("CUSTO DE VIDA FIXO (R$):", min_value=0.0, value=1500.0, key="custo_v",
                                      help="Opcional. Valor para aluguel, comida e contas. Não altera o valor da hora, apenas a sobra final.")
    
    st.markdown('<h4 style="color:#FFCC00">🚌 CUSTOS NO TRECHO (DIÁRIO)</h4>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1: p_pub = st.number_input("🚆 TRANSP. PÚBLICO", value=8.80)
    with g2: p_app = st.number_input("📱 APP/TÁXI", value=0.0)
    with g3: p_car = st.number_input("🚗 CARRO/COMBUST.", value=0.0)
    
    dias_m = st.number_input("DIAS DE TRECHO NO MÊS:", 1, 31, 22)
    h_dia = st.slider("TOTAL DE HORAS NO TRECHO (IDA+VOLTA):", 0.5, 12.0, 3.0, step=0.5)
    
    submit = st.form_submit_button("ANALISAR EXPROPRIAÇÃO")

if submit:
    # LÓGICA TÉCNICA BASEADA EM EXPROPRIAÇÃO
    h_pagas = 176
    v_hora_nom = sal_bruto / h_pagas
    custo_transp_mensal = (p_pub + p_app + p_car) * dias_m
    h_trecho_mensal = h_dia * dias_m
    
    # VALOR REAL DA HORA: (Salário - Gastos de Transporte) / (Horas de Trabalho + Horas de Trecho)
    v_hora_real = (sal_bruto - custo_transp_mensal) / (h_pagas + h_trecho_mensal)
    
    depreciacao_p = (1 - (v_hora_real / v_hora_nom)) * 100
    
    # VALOR NOMINAL DO CONFISCO: É a soma do gasto direto com transporte + o valor do tempo expropriado (h_trecho * valor da hora bruta)
    valor_tempo_perdido = h_trecho_mensal * v_hora_nom
    confisco_total = custo_transp_mensal + valor_tempo_perdido
    
    # RENDIMENTO RESIDUAL: O que sobra após transporte e custo de vida
    sobra = sal_bruto - custo_transp_mensal - custo_v

    # VETOR DE FLUXO (ESTILO TERMINAL)
    st.markdown(f"""
        <div style="background: #111; padding: 25px; border-radius: 10px; border: 1px solid #E63946; text-align: center; margin-top:20px;">
            <span style="color:#FFCC00; font-family:'Arial Black'; font-size:1.3rem;">🏠 {moradia}
