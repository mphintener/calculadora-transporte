import streamlit as st
import pandas as pd
from geodata import GEO_SPO 

# 1. IDENTIDADE VISUAL: PRETO, AMARELO E VERMELHO [cite: 2026-02-11]
st.set_page_config(page_title="Beta II - Calculadora do Trecho", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    
    /* TITULOS EM AMARELO ALTO CONTRASTE */
    label, .stSelectbox label, .stNumberInput label { 
        color: #FFCC00 !important; 
        font-weight: 800 !important; 
        text-transform: uppercase !important;
        font-size: 1.1rem !important;
    }

    .chamada-alerta { 
        background-color: #E63946; color: white; text-align: center; 
        padding: 15px; font-weight: 900; border: 4px solid #FFCC00; 
        margin-bottom: 20px; text-transform: uppercase; font-size: 1.6rem;
    }
    
    /* QUADROS DE RESULTADO TIPO TERMINAL */
    .sintese-box { 
        background-color: #111; border: 2px solid #FFCC00; 
        padding: 20px; margin-top: 10px; color: #FFFFFF; 
        font-family: 'Courier New', monospace; font-size: 1.1rem; line-height: 1.5;
    }
    
    .destaque-vermelho { color: #E63946; font-weight: 900; }
    .destaque-amarelo { color: #FFCC00; font-weight: bold; }

    /* INFOGRÁFICO DE TEMPO EXPROPRIADO */
    .barra-tempo {
        width: 100%; background-color: #333; height: 30px; border-radius: 5px; margin: 10px 0;
        display: flex; overflow: hidden; border: 1px solid #FFCC00;
    }
    .segmento-trabalho { background-color: #FFCC00; height: 100%; }
    .segmento-trecho { background-color: #E63946; height: 100%; }
    </style>
    """, unsafe_allow_html=True)

lista_geo = sorted(list(GEO_SPO.keys()))

st.markdown('<div class="chamada-alerta">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<h2 style="text-align:center; color:#FFCC00; text-transform:uppercase;">Quanto de tempo e de dinheiro são consumidos no seu deslocamento diário?</h2>', unsafe_allow_html=True)

with st.form("beta_ii_v16"):
    st.markdown('<div style="color:#FFCC00; font-weight:bold; border-bottom:1px solid #FFCC00; margin-bottom:15px;">📍 GEOGRAFIA E FLUXO</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: moradia = st.selectbox("ORIGEM (MORADIA):", lista_geo, index=0)
    with c2: trabalho = st.selectbox("DESTINO (TRABALHO):", lista_geo, index=1)
    
    st.markdown('<div style="color:#FFCC00; font-weight:bold; border-bottom:1px solid #FFCC00; margin:15px 0;">💵 RENDIMENTOS E SOBREVIVÊNCIA</div>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    with r1: sal_bruto = st.number_input("SALÁRIO BRUTO (R$):", min_value=0.0, step=100.0)
    with r2: custo_vida = st.number_input("CUSTO DE VIDA FIXO (R$):", min_value=0.0, step=50.0, help="Opcional. Gastos fixos que não alteram o valor da hora técnica.")
    
    st.markdown('<div style="color:#FFCC00; font-weight:bold; border-bottom:1px solid #FFCC00; margin:15px 0;">🚌 CUSTOS NO TRECHO (DIÁRIO)</div>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1: p_pub = st.number_input("🚆 ÔNIBUS/TREM", min_value=0.0, value=8.80)
    with g2: p_app = st.number_input("📱 APP/TÁXI", min_value=0.0)
    with g3: p_car = st.number_input("🚗 CARRO/MOTO", min_value=0.0)
    
    st.write("")
    d_m = st.number_input("DIAS DE TRECHO NO MÊS:", 1, 31, 22)
    h_d = st.slider("HORAS NO TRECHO POR DIA (TOTAL):", 0.5, 12.0, 3.0, step=0.5)
    
    btn_submit = st.form_submit_button("PROCESSAR DADOS DE IMPACTO")

if btn_submit:
    # LÓGICA TÉCNICA DINÂMICA [cite: 2026-02-11]
    h_pagas = 176
    v_hora_nom = sal_bruto / h_pagas if sal_bruto > 0 else 0
    custo_transp_mensal = (p_pub + p_app + p_car) * d_m
    h_expro_mensal = h_d * d_m
    
    # Rendimento Real: Salário sem transporte dividido pelo tempo total (trabalho + trecho)
    v_hora_real = (sal_bruto - custo_transp_mensal) / (h_pagas + h_expro_mensal) if sal_bruto > 0 else 0
    perda_p = (1 - (v_hora_real / v_hora_nom)) * 100 if v_hora_nom > 0 else 0
    confisco_monetario = sal_bruto * (perda_p / 100)
    sobra_residual = sal_bruto - custo_transp_mensal - custo_vida

    # VISUALIZAÇÃO: BARRA DE EXPROPRIAÇÃO DO DIA
    st.markdown('<div style="color:#FFCC00; font-weight:bold; margin-top:20px;">📊 IMPACTO NA JORNADA DIÁRIA (24H)</div>', unsafe_allow_html=True)
    pct_trabalho = (8 / 24) * 100
    pct_trecho = (h_d / 24) * 100
    st.markdown(f"""
        <div class="barra-tempo">
            <div class="segmento-trabalho" style="width: {pct_trabalho}%;"></div>
            <div class="segmento-trecho" style="width: {pct_trecho}%;"></div>
        </div>
        <p style="font-size:0.8rem; color:#AAA;">
            <span style="color:#FFCC00;">■</span> Trabalho Pago (8h) | 
            <span style="color:#E63946;">■</span> Trabalho Não Pago / Trecho ({h_d}h)
        </p>
    """, unsafe_allow_html=True)

    # SÍNTESE COMPACTA E INTEGRAL
    st.markdown('<div style="color:#FFCC00; font-weight:bold; margin-top:25px;">📝 SÍNTESE PARA COMUNICAÇÃO PÚBLICA</div>', unsafe_allow_html=True)
    sintese_txt = (f"MOBILIDADE GSP: O deslocamento entre {moradia} e {trabalho} é tempo de trabalho não pago que confisca {perda_p:.1f}% "
                   f"do seu rendimento. O valor da hora real cai para R$ {v_hora_real:.2f}.")
    st.markdown(f'<div class="sintese-box">{sintese_txt}</div>', unsafe_allow_html=True)

    # MÉTRICAS CONSOLIDADAS
    st.markdown('<div style="color:#FFCC00; font-weight:bold; margin-top:25px;">🔬 MÉTRICAS CONSOLIDADAS</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="sintese-box">
            • VALOR DA HORA: De R$ {v_hora_nom:.2f} para <span class="destaque-vermelho">R$ {v_hora_real:.2f}</span><br>
            • HORAS DE TRABALHO NÃO PAGAS: <span class="destaque-amarelo">{h_expro_mensal:.1f}h/mês</span><br>
            • VALOR NOMINAL DO CONFISCO: <span class="destaque-vermelho">R$ {confisco_monetario:,.2f}</span><br>
            • RENDIMENTO RESIDUAL (SOBRA): R$ {sobra_residual:,.2f}<br>
            • DEPRECIAÇÃO DA FORÇA DE TRABALHO: <span class="destaque-vermelho">{perda_p:.1f}%</span>
        </div>
    """, unsafe_allow_html=True)
