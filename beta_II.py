import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import pydeck as pdk
from geodata import GEO_SPO 

st.set_page_config(page_title="Beta II - Calculadora do Trecho", layout="centered")

# CSS: ALTO CONTRASTE (PRETO, AMARELO, VERMELHO)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    .chamada-impacto { background-color: #E63946; color: white; text-align: center; padding: 15px; font-weight: 900; border: 3px solid #FFCC00; margin-bottom: 25px; }
    .propisito-app { color: #FFCC00 !important; font-family: 'Arial Black', sans-serif; font-size: 1.8rem !important; text-align: center; text-transform: uppercase; }
    .secao-titulo { color: #FFCC00 !important; font-size: 1.1rem !important; font-weight: 800; text-transform: uppercase; margin-top: 25px; border-bottom: 2px solid #FFCC00; padding-bottom: 5px; }
    label { color: #FFCC00 !important; font-weight: 700 !important; }
    .card-res { background-color: #111; border: 1px solid #FFCC00; padding: 20px; text-align: center; border-radius: 8px; }
    .val-res { color: #FFCC00 !important; font-size: 2rem !important; font-weight: 900 !important; }
    .label-card { color: #FFFFFF !important; font-size: 0.8rem !important; font-weight: bold; text-transform: uppercase; }
    .sintese-box { background-color: #111; border-left: 10px solid #E63946; padding: 25px; margin-top: 30px; color: #FFFFFF; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

lista_geo = sorted(list(GEO_SPO.keys()))

st.markdown('<div class="chamada-impacto">LAB: EXPROPRIAÇÃO DO TEMPO</div>', unsafe_allow_html=True)
st.markdown('<div class="propisito-app">CALCULADORA DO TRECHO II</div>', unsafe_allow_html=True)

with st.form("beta_ii_fix"):
    col_g1, col_g2 = st.columns(2)
    with col_g1: moradia = st.selectbox("🏠 MORO EM:", lista_geo, index=lista_geo.index("Caieiras") if "Caieiras" in lista_geo else 0)
    with col_g2: trabalho = st.selectbox("💼 TRABALHO EM:", lista_geo, index=lista_geo.index("São Paulo (Centro)") if "São Paulo (Centro)" in lista_geo else 0)
    
    c1, c2, c3 = st.columns(3)
    with c1: sal = st.number_input("💵 SALÁRIO BRUTO (R$):", min_value=1.0, value=3000.0)
    with c2: vida = st.number_input("🏠 CUSTO VIDA (R$):", min_value=0.0, value=1500.0)
    with c3: dias = st.number_input("📅 DIAS NO TRECHO:", 1, 31, 22)
    
    st.markdown('<div class="secao-titulo">🚌 LOGÍSTICA DIÁRIA</div>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1: p_pub = st.number_input("🚆 PÚBLICO (R$)", 0.0, value=8.80)
    with g2: p_app = st.number_input("📱 APP (R$)", 0.0)
    with g3: p_car = st.number_input("🚗 PRIVADO (R$)", 0.0)
    
    h_trecho = st.slider("⏱️ HORAS NO TRECHO / DIA (IDA+VOLTA):", 0.5, 12.0, 3.0, step=0.5)
    btn = st.form_submit_button("CALCULAR IMPACTO REAL")

if btn:
    # CÁLCULOS TÉCNICOS
    h_paga_mes = 176
    custo_mes = (p_pub + p_app + p_car) * dias
    h_exprop_mes = h_trecho * dias
    v_hora_real = (sal - custo_mes) / (h_paga_mes + h_exprop_mes)
    perda_pct = (1 - (v_hora_real / (sal/h_paga_mes))) * 100
    sobra = sal - custo_mes - vida
    dias_ano = (h_exprop_mes * 12) / 24

    # CARDS DE RESULTADO
    res1, res2, res3 = st.columns(3)
    with res1: st.markdown(f'<div class="card-res"><div class="label-card">RENDIMENTO REAL<br>POR HORA</div><div class="val-res">R$ {v_hora_real:.2f}</div></div>', unsafe_allow_html=True)
    with res2: st.markdown(f'<div class="card-res"><div class="label-card">SALÁRIO REAL<br>CONFISCADO</div><div class="val-res">{perda_pct:.1f}%</div></div>', unsafe_allow_html=True)
    with res3: st.markdown(f'<div class="card-res"><div class="label-card">DIAS NO TRECHO<br>POR ANO</div><div class="val-res">{dias_ano:.1f}</div></div>', unsafe_allow_html=True)

    # MAPA CORRIGIDO (LIMPO E VISÍVEL)
    st.markdown('<div class="secao-titulo">🗺️ VETOR DE DESLOCAMENTO PENDULAR</div>', unsafe_allow_html=True)
    
    # IMPORTANTE: Pydeck usa [LON, LAT]
    m_lat, m_lon = GEO_SPO[moradia]
    t_lat, t_lon = GEO_SPO[trabalho]

    view_state = pdk.ViewState(latitude=(m_lat+t_lat)/2, longitude=(m_lon+t_lon)/2, zoom=10, pitch=0)
    
    layer_line = pdk.Layer(
        "LineLayer",
        data=[{"s": [m_lon, m_lat], "t": [t_lon, t_lat]}],
        get_source_position="s", get_target_position="t",
        get_color=[230, 57, 70], get_width=12
    )
    
    layer_points = pdk.Layer(
        "ScatterplotLayer",
        data=[{"p": [m_lon, m_lat], "c": [255, 204, 0]}, {"p": [t_lon, t_lat], "c": [230, 57, 70]}],
        get_position="p", get_color="c", get_radius=800
    )

    st.pydeck_chart(pdk.Deck(layers=[layer_line, layer_points], initial_view_state=view_state, map_style="mapbox://styles/mapbox/light-v10"))

    # RESUMO JORNALÍSTICO MELHORADO
    st.markdown('<div class="secao-titulo">📝 RESUMO PARA REPORTAGEM</div>', unsafe_allow_html=True)
    
    texto_jornal = (
        f"ANÁLISE DE MOBILIDADE: O deslocamento entre {moradia} e {trabalho} "
        f"reduz o valor real da hora trabalhada para R$ {v_hora_real:.2f}. "
        f"Isso representa um confisco de {perda_pct:.1f}% do rendimento bruto, "
        f"equivalente a {dias_ano:.1f} dias inteiros perdidos no trânsito por ano."
    )
    st.info(texto_jornal)
    st.code(texto_jornal, language="text")

    st.markdown(f"""
        <div class="sintese-box">
            <b>SÍNTESE DA EXPROPRIAÇÃO:</b><br>
            - Tempo não remunerado: {h_exprop_mes:.0f}h/mês<br>
            - Custo do transporte: R$ {custo_mes:,.2f}<br>
            - Rendimento residual (Sobra): <span style="color:#FFCC00">R$ {max(0, sobra):.2f}</span>
        </div>
    """, unsafe_allow_html=True)
