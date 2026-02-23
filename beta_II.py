import streamlit as st
import pandas as pd
import pydeck as pdk
from geodata import GEO_SPO 

# 1. ESTILO TERMINAL URBANO REFINADO
st.set_page_config(page_title="Beta II - Calculadora do Trecho", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    
    /* TÍTULOS E LABELS */
    label, .stSelectbox label { 
        color: #FFCC00 !important; 
        font-weight: 800 !important; 
        text-transform: uppercase !important;
    }
    
    /* TEXTO EXPLICATIVO (BRANCO PARA LEITURA) */
    .stMarkdown p, .stMarkdown div { color: #FFFFFF !important; }

    .chamada-alerta { 
        background-color: #E63946; color: white; text-align: center; 
        padding: 15px; font-weight: 900; border: 4px solid #FFCC00; 
        margin-bottom: 10px; text-transform: uppercase; font-size: 1.5rem;
    }
    
    .titulo-pergunta { 
        color: #FFCC00 !important; font-family: 'Arial Black', sans-serif; 
        font-size: 1.3rem !important; text-align: center; 
        text-transform: uppercase; margin-bottom: 30px;
    }

    .secao-titulo { 
        color: #FFCC00 !important; font-size: 1.1rem !important; font-weight: 800; 
        text-transform: uppercase; margin-top: 25px; border-bottom: 2px solid #FFCC00; padding-bottom: 5px; 
    }

    /* INPUTS LIMPAM E ACESSÍVEIS */
    .stNumberInput input {
        background-color: #111 !important;
        color: #FFFFFF !important;
        border: 1px solid #FFCC00 !important;
    }

    /* SÍNTESE COMPACTA */
    .sintese-box { 
        background-color: #111; border: 2px solid #FFCC00; 
        padding: 15px; margin-top: 10px; color: #FFFFFF; 
        font-family: monospace; font-size: 0.95rem; line-height: 1.4;
    }
    .destaque-vermelho { color: #E63946; font-weight: bold; }
    .destaque-amarelo { color: #FFCC00; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

lista_geo = sorted(list(GEO_SPO.keys()))

st.markdown('<div class="chamada-alerta">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="titulo-pergunta">Quanto de tempo e de dinheiro são consumidos no seu deslocamento diário?</div>', unsafe_allow_html=True)

with st.form("beta_ii_v11"):
    c_geo1, c_geo2 = st.columns(2)
    with c_geo1: moradia = st.selectbox("🏠 ORIGEM (MORADIA):", lista_geo, index=0)
    with c_geo2: trabalho = st.selectbox("💼 DESTINO (TRABALHO):", lista_geo, index=1)
    
    st.markdown('<div class="secao-titulo">💵 RENDIMENTOS E SOBREVIVÊNCIA</div>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    with r1: sal_bruto = st.number_input("SALÁRIO BRUTO MENSAL (R$):", min_value=0.0, value=3000.0)
    with r2: custo_vida = st.number_input("CUSTO DE VIDA FIXO (R$):", min_value=0.0, value=1500.0, help="Preenchimento opcional. Inclui aluguel, alimentação e contas.")
    
    st.markdown('<div class="secao-titulo">🚌 CUSTOS NO TRECHO (ÔNIBUS/METRÔ/APP/CARRO)</div>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1: p_pub = st.number_input("🚆 TRANSP. PÚBLICO (R$):", min_value=0.0, value=8.80)
    with g2: p_app = st.number_input("📱 APP/TÁXI (R$):", min_value=0.0)
    with g3: p_car = st.number_input("🚗 CARRO/COMBUST. (R$):", min_value=0.0)
    
    st.write("")
    d3, d4 = st.columns(2)
    with d3: dias_mes = st.number_input("DIAS NO TRECHO / MÊS:", 1, 31, 22)
    with d4: h_trecho = st.slider("HORAS NO TRECHO / DIA (TOTAL):", 0.5, 12.0, 3.0, step=0.5)
    
    btn = st.form_submit_button("EFETUAR CÁLCULO DE IMPACTO")

if btn:
    # LÓGICA TÉCNICA
    h_pagas_mes = 176
    custo_transp_mes = (p_pub + p_app + p_car) * dias_mes
    h_exprop_mes = h_trecho * dias_mes
    
    v_hora_nominal = sal_bruto / h_pagas_mes
    v_hora_real = (sal_bruto - custo_transp_mes) / (h_pagas_mes + h_exprop_mes)
    
    depreciacao_pct = (1 - (v_hora_real / v_hora_nominal)) * 100
    salario_confiscado = sal_bruto * (depreciacao_pct / 100)
    rendimento_residual = sal_bruto - custo_transp_mes - custo_vida
    dias_vida_ano = (h_exprop_mes * 12) / 24

    # MAPA (AJUSTE PARA NÃO "SUMIR")
    st.markdown('<div class="secao-titulo">🗺️ VETOR DE FLUXO PENDULAR</div>', unsafe_allow_html=True)
    m_lat, m_lon = GEO_SPO[moradia]
    t_lat, t_lon = GEO_SPO[trabalho]
    
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",
        initial_view_state=pdk.ViewState(latitude=(m_lat+t_lat)/2, longitude=(m_lon+t_lon)/2, zoom=10, pitch=40),
        layers=[pdk.Layer("ArcLayer", data=[{"s": [m_lon, m_lat], "t": [t_lon, t_lat]}], 
                get_source_position="s", get_target_position="t", 
                get_color=[230, 57, 70, 200], get_width=10)]
    ))

    # SÍNTESE COMPACTA (FONTES BRANCAS E AMARELAS)
    st.markdown('<div class="secao-titulo">📝 SÍNTESE PARA COMUNICAÇÃO PÚBLICA</div>', unsafe_allow_html=True)
    sintese_txt = (f"MOBILIDADE GSP: O trajeto {moradia}-{trabalho} confisca {depreciacao_pct:.1f}% do rendimento real. "
                   f"O valor da hora cai para R$ {v_hora_real:.2f}, resultando em {dias_vida_ano:.1f} dias perdidos/ano.")
    st.markdown(f'<div class="sintese-box">{sintese_txt}</div>', unsafe_allow_html=True)

    # MÉTRICAS CONSOLIDADAS (O COMPARATIVO)
    st.markdown('<div class="secao-titulo">🔬 MÉTRICAS CONSOLIDADAS DE EXPROPRIAÇÃO</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="sintese-box">
            • <span class="destaque-amarelo">VALOR DA HORA:</span> De R$ {v_hora_nominal:.2f} para <span class="destaque-vermelho">R$ {v_hora_real:.2f}</span><br>
            • <span class="destaque-amarelo">TEMPO MENSAL EXPROPRIADO:</span> {h_exprop_mes:.1f}h<br>
            • <span class="destaque-amarelo">CUSTO DE REPRODUÇÃO (TARIFAS):</span> R$ {custo_transp_mes:,.2f}<br>
            • <span class="destaque-amarelo">VALOR NOMINAL DO CONFISCO:</span> R$ {salario_confiscado:,.2f}<br>
            • <span class="destaque-amarelo">RENDIMENTO RESIDUAL (SOBRA FINAL):</span> R$ {rendimento_residual:,.2f}<br>
            • <span class="destaque-amarelo">DEPRECIAÇÃO REAL DA HORA:</span> {depreciacao_pct:.1f}%
        </div>
    """, unsafe_allow_html=True)
