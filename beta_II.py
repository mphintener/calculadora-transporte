import streamlit as st
import pandas as pd
import pydeck as pdk
from geodata import GEO_SPO 

# 1. ESTILO TERMINAL URBANO
st.set_page_config(page_title="Beta II - Calculadora do Trecho", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    
    /* LABELS EM AMARELO */
    label, p, span { 
        color: #FFCC00 !important; 
        font-weight: 800 !important; 
        text-transform: uppercase !important;
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
        color: #FFCC00 !important; font-size: 1.1rem !important; font-weight: 800; 
        text-transform: uppercase; margin-top: 25px; border-bottom: 2px solid #FFCC00; padding-bottom: 5px; 
    }

    /* LIMPEZA DOS INPUTS */
    .stNumberInput div[data-baseweb="input"] { background-color: #111 !important; border: 1px solid #FFCC00 !cite: 2 !important; }
    .stNumberInput input { color: #FFFFFF !important; font-size: 1.2rem !important; }

    .sintese-box { 
        background-color: #111; border: 2px solid #FFCC00; 
        padding: 20px; margin-top: 20px; color: #FFFFFF; 
        font-family: 'Courier New', monospace;
    }
    </style>
    """, unsafe_allow_html=True)

lista_geo = sorted(list(GEO_SPO.keys()))

st.markdown('<div class="chamada-alerta">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="titulo-pergunta">Quanto de tempo e de dinheiro são consumidos no seu deslocamento diário?</div>', unsafe_allow_html=True)

with st.form("beta_ii_v10"):
    c1, c2 = st.columns(2)
    with c1: moradia = st.selectbox("🏠 ORIGEM:", lista_geo, index=0)
    with c2: trabalho = st.selectbox("💼 DESTINO:", lista_geo, index=1)
    
    st.markdown('<div class="secao-titulo">💵 RENDIMENTOS E SOBREVIVÊNCIA</div>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    with r1: sal = st.number_input("SALÁRIO BRUTO:", min_value=1.0, value=3000.0)
    with r2: vida = st.number_input("CUSTO DE VIDA (OPCIONAL):", min_value=0.0, value=1500.0)
    
    st.markdown('<div class="secao-titulo">🚌 CUSTOS E TEMPO NO TRECHO</div>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1: p_pub = st.number_input("🚆 TRANSP. PÚBLICO", min_value=0.0, value=8.80)
    with g2: p_app = st.number_input("📱 APP/TÁXI", min_value=0.0)
    with g3: p_car = st.number_input("🚗 CARRO/MOTO", min_value=0.0)
    
    col_d, col_h = st.columns(2)
    with col_d: dias = st.number_input("DIAS NO TRECHO/MÊS:", 1, 31, 22)
    with col_h: h_trecho = st.slider("HORAS NO TRECHO (DIA):", 0.5, 12.0, 3.0, step=0.5)
    
    btn = st.form_submit_button("PROCESSAR DADOS DE IMPACTO")

if btn:
    # LÓGICA TÉCNICA
    h_pagas_mes = 176
    custo_transp_mes = (p_pub + p_app + p_car) * dias
    h_exprop_mes = h_trecho * dias
    
    # Rendimento Real por Hora: (Salário - Tarifas) / (Horas Pagas + Horas Trecho)
    v_hora_real = (sal - custo_transp_mes) / (h_pagas_mes + h_exprop_mes)
    perda_pct = (1 - (v_hora_real / (sal/h_pagas_mes))) * 100
    sobra_final = sal - custo_transp_mes - vida
    dias_ano = (h_exprop_mes * 12) / 24

    # MAPA VETORIAL
    st.markdown('<div class="secao-titulo">🗺️ VETOR DE FLUXO PENDULAR</div>', unsafe_allow_html=True)
    m_lat, m_lon = GEO_SPO[moradia]
    t_lat, t_lon = GEO_SPO[trabalho]
    st.pydeck_chart(pdk.Deck(
        map_style=pdk.map_styles.DARK,
        initial_view_state=pdk.ViewState(latitude=(m_lat+t_lat)/2, longitude=(m_lon+t_lon)/2, zoom=10, pitch=45),
        layers=[pdk.Layer("ArcLayer", data=[{"s": [m_lon, m_lat], "t": [t_lon, t_lat]}], 
                get_source_position="s", get_target_position="t", 
                get_color=[230, 57, 70, 200], get_width=12)]
    ))

    # SÍNTESE JORNALÍSTICA
    st.markdown('<div class="secao-titulo">📝 SÍNTESE PARA COMUNICAÇÃO PÚBLICA</div>', unsafe_allow_html=True)
    sintese = (f"MOBILIDADE GSP: O trecho {moradia}-{trabalho} confisca {perda_pct:.1f}% do salário real. "
               f"O valor da hora cai para R$ {v_hora_real:.2f}, resultando em {dias_ano:.1f} dias perdidos/ano.")
    st.code(sintese, language="text")

    # RELATÓRIO TÉCNICO
    st.markdown('<div class="secao-titulo">🔬 MÉTRICAS CONSOLIDADAS DE EXPROPRIAÇÃO</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="sintese-box">
            • TEMPO MENSAL EXPROPRIADO: {h_exprop_mes:.1f}h<br>
            • CUSTO DE REPRODUÇÃO (TARIFAS): R$ {custo_transp_mes:,.2f}<br>
            • RENDIMENTO RESIDUAL (SOBRA FINAL): R$ {sobra_final:,.2f}<br>
            • SALÁRIO REAL CONFISCADO: {perda_pct:.1f}%
        </div>
    """, unsafe_allow_html=True)
