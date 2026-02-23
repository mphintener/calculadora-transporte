import streamlit as st
import pandas as pd
import pydeck as pdk
from geodata import GEO_SPO 

st.set_page_config(page_title="Beta II - Calculadora do Trecho", layout="centered")

# CSS: CORREÇÃO DE VISIBILIDADE E CORES
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    
    /* TÍTULOS DOS BLOCOS (CORRIGIDO PARA AMARELO) */
    .stSelectbox label, .stNumberInput label, .stSlider label { 
        color: #FFCC00 !important; 
        font-weight: 800 !important; 
        text-transform: uppercase !important;
        font-size: 0.85rem !important;
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
    .card-res { background-color: #111; border: 1px solid #FFCC00; padding: 15px; text-align: center; border-radius: 8px; }
    .val-res { color: #FFCC00 !important; font-size: 1.8rem !important; font-weight: 900 !important; }
    .label-card { color: #FFFFFF !important; font-size: 0.75rem !important; font-weight: bold; text-transform: uppercase; }
    
    /* SÍNTESE COMPACTA */
    .sintese-box { background-color: #111; border-left: 10px solid #E63946; padding: 15px; margin-top: 20px; color: #FFFFFF; font-family: monospace; font-size: 0.9rem; line-height: 1.4; }
    </style>
    """, unsafe_allow_html=True)

lista_geo = sorted(list(GEO_SPO.keys()))

st.markdown('<div class="chamada-alerta">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="titulo-pergunta">Quanto de salário e de tempo você perde no seu deslocamento diário?</div>', unsafe_allow_html=True)

with st.form("beta_ii_v4"):
    col_g1, col_g2 = st.columns(2)
    with col_g1: moradia = st.selectbox("🏠 ORIGEM (MORADIA):", lista_geo, index=0)
    with col_g2: trabalho = st.selectbox("💼 DESTINO (TRABALHO):", lista_geo, index=1)
    
    c1, c2, c3 = st.columns(3)
    with c1: sal = st.number_input("💵 SALÁRIO BRUTO:", min_value=1.0, value=3000.0)
    with c2: vida = st.number_input("🏠 CUSTO VIDA:", min_value=0.0, value=1500.0)
    with c3: dias = st.number_input("📅 DIAS NO TRECHO/MÊS:", 1, 31, 22)
    
    st.markdown('<div class="secao-titulo">🚌 LOGÍSTICA DE DESLOCAMENTO</div>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1: p_pub = st.number_input("🚆 PÚBLICO (R$)", 0.0, value=8.80)
    with g2: p_app = st.number_input("📱 APP (R$)", 0.0)
    with g3: p_car = st.number_input("🚗 PRIVADO (R$)", 0.0)
    
    h_trecho = st.slider("⏱️ HORAS NO TRECHO / DIA (TOTAL):", 0.5, 12.0, 3.0, step=0.5)
    btn = st.form_submit_button("PROCESSAR DADOS")

if btn:
    # LÓGICA TÉCNICA (CORRIGIDA PARA VARIAR RENDIMENTO HORA)
    h_paga_mes = 176
    custo_transp_mes = (p_pub + p_app + p_car) * dias
    h_exprop_mes = h_trecho * dias
    
    # O valor da hora nominal (sem transporte)
    v_hora_nominal = sal / h_paga_mes
    # O valor da hora REAL (salário limpo dividido pelo tempo total dedicado ao capital)
    v_hora_real = (sal - custo_transp_mes) / (h_paga_mes + h_exprop_mes)
    
    perda_pct = (1 - (v_hora_real / v_hora_nominal)) * 100
    confisco_monetario = sal * (perda_pct / 100)
    sobra_final = sal - custo_transp_mes - vida
    dias_ano_perdidos = (h_exprop_mes * 12) / 24

    r1, r2, r3 = st.columns(3)
    with r1: st.markdown(f'<div class="card-res"><div class="label-card">RENDIMENTO REAL<br>POR HORA</div><div class="val-res">R$ {v_hora_real:.2f}</div></div>', unsafe_allow_html=True)
    with r2: st.markdown(f'<div class="card-res"><div class="label-card">SALÁRIO REAL<br>CONFISCADO</div><div class="val-res">{perda_pct:.1f}%</div></div>', unsafe_allow_html=True)
    with r3: st.markdown(f'<div class="card-res"><div class="label-card">DIAS NO TRECHO<br>POR ANO</div><div class="val-res">{dias_ano_perdidos:.1f}</div></div>', unsafe_allow_html=True)

    # MAPA COM ZOOM E FUNDO ESCURO (CORRIGIDO)
    st.markdown('<div class="secao-titulo">🗺️ VETOR DE FLUXO PENDULAR (GSP)</div>', unsafe_allow_html=True)
    m_lat, m_lon = GEO_SPO[moradia]
    t_lat, t_lon = GEO_SPO[trabalho]

    st.pydeck_chart(pdk.Deck(
        map_style=pdk.map_styles.DARK,
        initial_view_state=pdk.ViewState(
            latitude=(m_lat+t_lat)/2, longitude=(m_lon+t_lon)/2, 
            zoom=10.5, pitch=40
        ),
        layers=[
            pdk.Layer(
                "ArcLayer",
                data=[{"s": [m_lon, m_lat], "t": [t_lon, t_lat]}],
                get_source_position="s", get_target_position="t",
                get_source_color=[255, 204, 0, 200], get_target_color=[230, 57, 70, 200],
                get_width=10
            )
        ]
    ))

    # SÍNTESE COMPACTADA PARA IMPRENSA
    st.markdown('<div class="secao-titulo">📝 SÍNTESE PARA COMUNICAÇÃO PÚBLICA</div>', unsafe_allow_html=True)
    sintese = (f"MOBILIDADE GSP: O trecho {moradia}-{trabalho} confisca {perda_pct:.1f}% do salário real. "
               f"O valor da hora cai de R$ {v_hora_nominal:.2f} para R$ {v_hora_real:.2f}, "
               f"implicando em {dias_ano_perdidos:.1f} dias perdidos/ano.")
    st.code(sintese, language="text")

    # RELATÓRIO TÉCNICO COMPLETO
    st.markdown('<div class="secao-titulo">🔬 RELATÓRIO TÉCNICO DE EXPROPRIAÇÃO</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="sintese-box">
            <b>MÉTRICAS CONSOLIDADAS:</b><br>
            • Tempo Mensal Expropriado: {h_exprop_mes:.1f}h<br>
            • Custo de Reprodução (Tarifas): R$ {custo_transp_mes:,.2f}<br>
            • Valor Nominal do Confisco: R$ {confisco_monetario:,.2f}<br>
            • Rendimento Residual (Sobra Final): R$ {sobra_final:,.2f}<br>
            • Depreciação da Hora de Trabalho: {perda_pct:.1f}%
        </div>
    """, unsafe_allow_html=True)
