import streamlit as st
import pandas as pd
from geodata import GEO_SPO 

# 1. IDENTIDADE VISUAL E AJUSTES DE INTERAÇÃO
st.set_page_config(page_title="Beta II - Calculadora do Trecho", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    
    /* LABELS EM AMARELO NÍTIDO */
    label, .stSelectbox label, .stNumberInput label { 
        color: #FFCC00 !important; font-weight: 800 !important; 
        text-transform: uppercase !important; font-size: 0.9rem !important;
    }

    .chamada-alerta { 
        background-color: #E63946; color: white; text-align: center; 
        padding: 10px; font-weight: 900; border: 2px solid #FFCC00; 
        margin-bottom: 8px; text-transform: uppercase; font-size: 1.2rem;
    }
    
    .titulo-pergunta { 
        color: #FFCC00 !important; font-family: 'Arial', sans-serif; 
        font-size: 1.1rem !important; text-align: center; 
        text-transform: uppercase; margin-bottom: 25px;
    }

    /* INPUTS TOTALMENTE EDITÁVEIS */
    .stNumberInput input { background-color: #111 !important; color: #FFFFFF !important; border: 1px solid #444 !important; }

    .sintese-box { 
        background-color: #111; border: 1px solid #FFCC00; 
        padding: 18px; margin-top: 10px; color: #FFFFFF; 
        font-family: 'Courier New', monospace; font-size: 1rem;
    }
    
    .expro-destaque { color: #E63946; font-weight: 900; }
    .valor-amarelo { color: #FFCC00; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

lista_geo = sorted(list(GEO_SPO.keys()))

st.markdown('<div class="chamada-alerta">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="titulo-pergunta">Quanto de tempo e de dinheiro são consumidos no seu deslocamento diário?</div>', unsafe_allow_html=True)

with st.form("form_beta_ii_v11"):
    st.markdown('<h4 style="color:#FFCC00">📍 GEOGRAFIA E FLUXO</h4>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: moradia = st.selectbox("MORADIA (ORIGEM):", lista_geo, index=0)
    with c2: trabalho = st.selectbox("TRABALHO (DESTINO):", lista_geo, index=1)
    
    st.markdown('<h4 style="color:#FFCC00">💵 RENDIMENTOS E SOBREVIVÊNCIA</h4>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    with r1: sal_bruto = st.number_input("SALÁRIO BRUTO (R$):", min_value=0.0, value=3000.0)
    with r2: custo_vida = st.number_input("CUSTO DE VIDA FIXO (R$):", min_value=0.0, value=1500.0, help="Opcional. Gastos de sobrevivência. Não afeta o confisco, apenas a sobra final.")
    
    st.markdown('<h4 style="color:#FFCC00">🚌 CUSTOS NO TRECHO (ÔNIBUS/METRÔ/TREM/APP/CARRO)</h4>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1: p_pub = st.number_input("🚆 TRANSP. PÚBLICO (R$)", value=8.80)
    with g2: p_app = st.number_input("📱 APP/TÁXI (R$)", value=0.0)
    with g3: p_car = st.number_input("🚗 CARRO/COMBUST. (R$)", value=0.0)
    
    dias_m = st.number_input("DIAS DE TRECHO NO MÊS:", 1, 31, 22)
    h_dia = st.slider("TOTAL DE HORAS NO TRECHO / DIA:", 0.5, 12.0, 3.0, step=0.5)
    
    submit = st.form_submit_button("EFETUAR CÁLCULO TÉCNICO")

if submit:
    # LÓGICA TÉCNICA REFINADA
    h_pagas_mensais = 176
    v_hora_nominal = sal_bruto / h_pagas_mensais
    
    custo_transp_diario = p_pub + p_app + p_car
    custo_transp_mensal = custo_transp_diario * dias_m
    h_trecho_mensal = h_dia * dias_m
    
    # CONFISCO NOMINAL: (Horas no Trecho * Valor Hora Nominal) + Gastos com Transporte
    # O Custo de Vida NÃO entra aqui.
    valor_tempo_expropriado = h_trecho_mensal * v_hora_nominal
    confisco_total = custo_transp_mensal + valor_tempo_expropriado
    
    # VALOR REAL DA HORA: Salário líquido de transporte / (Horas Pagas + Horas Trecho)
    v_hora_real = (sal_bruto - custo_transp_mensal) / (h_pagas_mensais + h_trecho_mensal)
    
    depreciacao_pct = (1 - (v_hora_real / v_hora_nominal)) * 100
    sobra_residual = sal_bruto - custo_transp_mensal - custo_vida

    # VETOR DE FLUXO PENDULAR DETALHADO
    st.markdown('<h4 style="color:#FFCC00">🗺️ VETOR DE DESLOCAMENTO PENDULAR</h4>', unsafe_allow_html=True)
    st.markdown(f"""
        <div style="background: #111; padding: 25px; border: 1px solid #E63946; text-align: center;">
            <div style="display: flex; justify-content: space-around; align-items: center;">
                <div style="color: #FFCC00;"><b>🏠 {moradia}</b><br><small>{h_dia/2}h</small></div>
                <div style="color: #E63946; font-size: 1.5rem;">⚡――――▶</div>
                <div style="color: #FFCC00;"><b>💼 {trabalho}</b><br><small>{h_dia/2}h</small></div>
            </div>
            <p style="color:#E63946; font-size:0.9rem; margin-top:15px; font-weight:bold; border-top: 1px solid #333; padding-top:10px;">
                CASA-TRABALHO-CASA É TEMPO DE TRABALHO NÃO PAGO
            </p>
        </div>
    """, unsafe_allow_html=True)

    # SÍNTESE
    st.markdown('<h4 style="color:#FFCC00">📝 SÍNTESE DA EXPROPRIAÇÃO</h4>', unsafe_allow_html=True)
    sintese_txt = (f"MOBILIDADE GSP: Ao se deslocar entre {moradia} e {
