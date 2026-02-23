import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import pydeck as pdk
from geodata import GEO_SPO  # Importa sua base de 96 distritos e 38 cidades

# 1. CONFIGURAÇÃO DE TELA E IDENTIDADE VISUAL
st.set_page_config(page_title="Beta II - Calculadora do Trecho", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    .chamada-impacto { 
        background-color: #E63946; color: white; text-align: center; 
        padding: 15px; font-weight: 900; text-transform: uppercase; 
        border: 3px solid #FFCC00; margin-bottom: 25px; font-size: 1.5rem; 
    }
    .propisito-app { 
        color: #FFCC00 !important; font-family: 'Arial Black', sans-serif; 
        font-size: 1.8rem !important; text-align: center; text-transform: uppercase; 
    }
    .secao-titulo { 
        color: #FFCC00 !important; font-size: 1.1rem !important; font-weight: 800; 
        text-transform: uppercase; margin-top: 25px; border-bottom: 2px solid #FFCC00; padding-bottom: 5px; 
    }
    label { color: #FFCC00 !important; font-weight: 700 !important; font-size: 0.9rem !important; }
    
    .card-res { 
        background-color: #111; border: 2px solid #333; padding: 20px 10px; 
        text-align: center; border-radius: 8px; min-height: 160px; 
    }
    .val-res { color: #FFCC00 !important; font-size: 2.2rem !important; font-weight: 900 !important; }
    .label-card { color: #FFFFFF !important; font-size: 0.7rem !important; font-weight: bold; text-transform: uppercase; }
    
    .sintese-box { 
        background-color: #111; border-left: 10px solid #E63946; 
        padding: 30px; margin-top: 40px; color: #FFFFFF; font-family: monospace; 
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CARREGAMENTO DA BASE GEOGRÁFICA
lista_geo = sorted(list(GEO_SPO.keys()))

st.markdown('<div class="chamada-impacto">LAB: EXPROPRIAÇÃO DO TEMPO</div>', unsafe_allow_html=True)
st.markdown('<div class="propisito-app">CALCULADORA DO TRECHO II</div>', unsafe_allow_html=True)

# 3. FORMULÁRIO DE ENTRADA
with st.form("beta_ii_form"):
    col_geo1, col_geo2 = st.columns(2)
    with col_geo1: moradia = st.selectbox("🏠 MORO EM:", lista_geo)
    with col_geo2: trabalho = st.selectbox("💼 TRABALHO EM:", lista_geo)
    
    c1, c2, c3 = st.columns(3)
    with c1: sal = st.number_input("💵 SALÁRIO BRUTO:", min_value=1.0, value=3000.0)
    with c2: vida = st.number_input("🏠 CUSTO VIDA:", min_value=0.0, value=1500.0)
    with c3: dias_presenca = st.number_input("📅 DIAS NO TRECHO/MÊS:", 1, 31, 22)
    
    st.markdown('<div class="secao-titulo">🚌 GASTOS E TEMPO DIÁRIO</div>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1: p_pub = st.number_input("🚆 PÚBLICO (R$)", 0.0, value=8.80)
    with g2: p_app = st.number_input("📱 APP (R$)", 0.0)
    with g3: p_car = st.number_input("🚗 PRIVADO (R$)", 0.0)
    
    h_trecho = st.slider("⏱️ HORAS NO TRECHO POR DIA (IDA+VOLTA):", 0.5, 12.0, 3.0, step=0.5)
    btn = st.form_submit_button("ANALISAR DADOS DE MOBILIDADE")

# 4. LÓGICA E RESULTADOS
if btn:
    h_paga_mes = 176
    custo_transp_mes = (p_pub + p_app + p_car) * dias_presenca
    h_total_exprop_mes = h_trecho * dias_presenca
    
    # Rendimento Real considerando a expropriação do tempo
    v_hora_real = (sal - custo_transp_mes) / (h_paga_mes + h_total_exprop_mes)
    perda_pct = (1 - (v_hora_real / (sal/h_paga_mes))) * 100
    sobra_final = sal - custo_transp_mes - vida
    
    # Métrica: Dias de vida perdidos por ano
    dias_no_trecho_ano = (h_total_exprop_mes * 12) / 24

    r1, r2, r3 = st.columns(3)
    with r1: st.markdown(f'<div class="card-res"><div class="label-card">RENDIMENTO REAL<br>POR HORA</div><div class="val-res">R$ {v_hora_real:.2f}</div></div>', unsafe_allow_html=True)
    with r2: st.markdown(f'<div class="card-res"><div class="label-card">SALÁRIO REAL<br>CONFISCADO</div><div class="val-res">{perda_pct:.1f}%</div></div>', unsafe_allow_html=True)
    with r3: st.markdown(f'<div class="card-res"><div class="label-card">TEMPO NO TRECHO<br>POR ANO</div><div class="val-res">{dias_no_trecho_ano:.1f} DIAS</div></div>', unsafe_allow_html=True)

    # 5. MAPA CLEAN (CONCEITO JORNALÍSTICO)
    st.markdown('<div class="secao-titulo">🗺️ VETOR DE DESLOCAMENTO PENDULAR</div>', unsafe_allow_html=True)
    
    # Puxando coordenadas do geodata.py
    line_data = [{
        "source": [GEO_SPO[moradia][1], GEO_SPO[moradia][0]],
        "target": [GEO_SPO[trabalho][1], GEO_SPO[trabalho][0]]
    }]

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v10',
        initial_view_state=pdk.ViewState(
            latitude=(GEO_SPO[moradia][0] + GEO_SPO[trabalho][0]) / 2,
            longitude=(GEO_SPO[moradia][1] + GEO_SPO[trabalho][1]) / 2,
            zoom=10, pitch=0
        ),
        layers=[
            pdk.Layer("LineLayer", data=line_data, get_source_position="source", 
                      get_target_position="target", get_color=[230, 57, 46], get_width=10),
            pdk.Layer("ScatterplotLayer", data=[{"pos": [GEO_SPO[moradia][1], GEO_SPO[moradia][0]]}],
                      get_position="pos", get_color=[255, 204, 0], get_radius=700),
            pdk.Layer("ScatterplotLayer", data=[{"pos": [GEO_SPO[trabalho][1], GEO_SPO[trabalho][0]]}],
                      get_position="pos", get_color=[230, 57, 46], get_radius=700),
        ]
    ))

    # 6. SÍNTESE PARA IMPRENSA
    st.markdown('<div class="secao-titulo">📝 RESUMO PARA REPORTAGEM</div>', unsafe_allow_html=True)
    resumo = f"O trajeto entre {moradia} e {trabalho} confisca {perda_pct:.1f}% do salário real. Ao ano, são {dias_no_trecho_ano:.1f} dias perdidos no trecho."
    st.code(resumo, language="text")

    st.markdown(f"""
        <div class="sintese-box">
            <b>RELATÓRIO DE IMPACTO:</b><br>
            - Expropriação mensal: {h_total_exprop_mes:.0f}h<br>
            - Custo transporte: R$ {custo_transp_mes:,.2f}<br>
            - Sobra final: <span style="color:#FFCC00">R$ {sobra_final:,.2f}</span>
        </div>
    """, unsafe_allow_html=True)
