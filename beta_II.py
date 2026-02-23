import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import pydeck as pdk
from geodata import GEO_SPO 

# 1. CONFIGURAÇÃO DE TELA E CSS
st.set_page_config(page_title="Beta II - Calculadora do Trecho", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    
    /* CHAMADA ALERTA DE EXPROPRIAÇÃO MENSAL */
    .chamada-alerta { 
        background-color: #E63946; color: white; text-align: center; 
        padding: 15px; font-weight: 900; border: 4px solid #FFCC00; 
        margin-bottom: 10px; text-transform: uppercase; font-size: 1.6rem;
    }
    
    /* TÍTULO PRINCIPAL */
    .titulo-pergunta { 
        color: #FFCC00 !important; font-family: 'Arial Black', sans-serif; 
        font-size: 1.5rem !important; text-align: center; 
        text-transform: uppercase; margin-bottom: 30px; line-height: 1.2;
    }

    .secao-titulo { 
        color: #FFCC00 !important; font-size: 1.1rem !important; font-weight: 800; 
        text-transform: uppercase; margin-top: 25px; border-bottom: 2px solid #FFCC00; padding-bottom: 5px; 
    }
    label { color: #FFCC00 !important; font-weight: 700 !important; }
    
    .card-res { background-color: #111; border: 1px solid #FFCC00; padding: 20px; text-align: center; border-radius: 8px; }
    .val-res { color: #FFCC00 !important; font-size: 2.2rem !important; font-weight: 900 !important; }
    .label-card { color: #FFFFFF !important; font-size: 0.8rem !important; font-weight: bold; text-transform: uppercase; }
    
    .sintese-box { background-color: #111; border-left: 10px solid #E63946; padding: 25px; margin-top: 30px; color: #FFFFFF; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

lista_geo = sorted(list(GEO_SPO.keys()))

# 2. CABEÇALHO DE IMPACTO
st.markdown('<div class="chamada-alerta">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="titulo-pergunta">Quanto de salário e de tempo você perde no seu deslocamento diário?</div>', unsafe_allow_html=True)

# 3. FORMULÁRIO
with st.form("beta_ii_impacto"):
    col_g1, col_g2 = st.columns(2)
    with col_g1: moradia = st.selectbox("🏠 MORO EM:", lista_geo, index=lista_geo.index("Caieiras") if "Caieiras" in lista_geo else 0)
    with col_g2: trabalho = st.selectbox("💼 TRABALHO EM:", lista_geo, index=lista_geo.index("São Paulo (Centro)") if "São Paulo (Centro)" in lista_geo else 0)
    
    c1, c2, c3 = st.columns(3)
    with c1: sal = st.number_input("💵 SALÁRIO BRUTO (R$):", min_value=1.0, value=3000.0)
    with c2: vida = st.number_input("🏠 CUSTO VIDA (R$):", min_value=0.0, value=1500.0)
    with c3: dias = st.number_input("📅 DIAS NO TRECHO:", 1, 31, 22)
    
    st.markdown('<div class="secao-titulo">🚌 LOGÍSTICA E CUSTOS</div>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1: p_pub = st.number_input("🚆 PÚBLICO (R$)", 0.0, value=8.80)
    with g2: p_app = st.number_input("📱 APP (R$)", 0.0)
    with g3: p_car = st.number_input("🚗 PRIVADO (R$)", 0.0)
    
    h_trecho = st.slider("⏱️ HORAS NO TRECHO / DIA (TOTAL):", 0.5, 12.0, 3.0, step=0.5)
    btn = st.form_submit_button("ANALISAR EXPROPRIAÇÃO")

# 4. RESULTADOS
if btn:
    h_paga_mes = 176
    custo_mes = (p_pub + p_app + p_car) * dias
    h_exprop_mes = h_trecho * dias
    v_hora_real = (sal - custo_mes) / (h_paga_mes + h_exprop_mes)
    perda_pct = (1 - (v_hora_real / (sal/h_paga_mes))) * 100
    sobra = sal - custo_mes - vida
    dias_ano = (h_exprop_mes * 12) / 24

    res1, res2, res3 = st.columns(3)
    with res1: st.markdown(f'<div class="card-res"><div class="label-card">RENDIMENTO REAL<br>POR HORA</div><div class="val-res">R$ {v_hora_real:.2f}</div></div>', unsafe_allow_html=True)
    with res2: st.markdown(f'<div class="card-res"><div class="label-card">SALÁRIO REAL<br>CONFISCADO</div><div class="val-res">{perda_pct:.1f}%</div></div>', unsafe_allow_html=True)
    with res3: st.markdown(f'<div class="card-res"><div class="label-card">DIAS NO TRECHO<br>POR ANO</div><div class="val-res">{dias_ano:.1f}</div></div>', unsafe_allow_html=True)

    # MAPA ROBUSTO
    st.markdown('<div class="secao-titulo">🗺️ VETOR DE DESLOCAMENTO PENDULAR</div>', unsafe_allow_html=True)
    m_lat, m_lon = GEO_SPO[moradia]
    t_lat, t_lon = GEO_SPO[trabalho]

    st.pydeck_chart(pdk.Deck(
        map_style=pdk.map_styles.ROAD,
        initial_view_state=pdk.ViewState(latitude=(m_lat+t_lat)/2, longitude=(m_lon+t_lon)/2, zoom=10),
        layers=[
            pdk.Layer("LineLayer", data=[{"s": [m_lon, m_lat], "t": [t_lon, t_lat]}], 
                      get_source_position="s", get_target_position="t", get_color=[230, 57, 70], get_width=15),
            pdk.Layer("ScatterplotLayer", data=[{"p": [m_lon, m_lat], "c": [255, 204, 0]}, {"p": [t_lon, t_lat], "c": [230, 57, 70]}],
                      get_position="p", get_color="c", get_radius=800)
        ]
    ))

    # RESUMO PARA REPORTAGEM
    st.markdown('<div class="secao-titulo">📝 RESUMO PARA REPORTAGEM</div>', unsafe_allow_html=True)
    texto_jornal = (
        f"ANÁLISE DE MOBILIDADE: O deslocamento entre {moradia} e {trabalho} "
        f"reduz o valor real da hora trabalhada para R$ {v_hora_real:.2f}. "
        f"Isso representa um confisco de {perda_pct:.1f}% do rendimento bruto, "
        f"equivalente a {dias_ano:.1f} dias inteiros perdidos no trânsito por ano."
    )
    st.code(texto_jornal, language="text")

    st.markdown(f"""
        <div class="sintese-box">
            <b>RELATÓRIO TÉCNICO:</b><br>
            - Tempo expropriado: {h_exprop_mes:.0f}h/mês<br>
            - Custo transporte: R$ {custo_mes:,.2f}<br>
            - Sobra final (Rendimento Residual): <span style="color:#FFCC00">R$ {max(0, sobra):.2f}</span>
        </div>
    """, unsafe_allow_html=True)
