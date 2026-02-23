import streamlit as st
import pandas as pd
import pydeck as pdk
from geodata import GEO_SPO 

st.set_page_config(page_title="Beta II - Calculadora do Trecho", layout="centered")

# CSS: ALTO CONTRASTE E ESTILO ACADÊMICO-CRÍTICO
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    .chamada-alerta { 
        background-color: #E63946; color: white; text-align: center; 
        padding: 15px; font-weight: 900; border: 4px solid #FFCC00; 
        margin-bottom: 10px; text-transform: uppercase; font-size: 1.6rem;
    }
    .titulo-pergunta { 
        color: #FFCC00 !important; font-family: 'Arial Black', sans-serif; 
        font-size: 1.5rem !important; text-align: center; 
        text-transform: uppercase; margin-bottom: 30px;
    }
    .secao-titulo { 
        color: #FFCC00 !important; font-size: 1.1rem !important; font-weight: 800; 
        text-transform: uppercase; margin-top: 25px; border-bottom: 2px solid #FFCC00; padding-bottom: 5px; 
    }
    .card-res { background-color: #111; border: 1px solid #FFCC00; padding: 20px; text-align: center; border-radius: 8px; }
    .val-res { color: #FFCC00 !important; font-size: 2.2rem !important; font-weight: 900 !important; }
    .label-card { color: #FFFFFF !important; font-size: 0.8rem !important; font-weight: bold; text-transform: uppercase; }
    .sintese-box { background-color: #111; border-left: 10px solid #E63946; padding: 25px; margin-top: 30px; color: #FFFFFF; font-family: monospace; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

lista_geo = sorted(list(GEO_SPO.keys()))

st.markdown('<div class="chamada-alerta">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="titulo-pergunta">Quanto de salário e de tempo você perde no seu deslocamento diário?</div>', unsafe_allow_html=True)

with st.form("beta_ii_final_v3"):
    col_g1, col_g2 = st.columns(2)
    with col_g1: moradia = st.selectbox("🏠 ORIGEM (MORADIA):", lista_geo, index=0)
    with col_g2: trabalho = st.selectbox("💼 DESTINO (TRABALHO):", lista_geo, index=1)
    
    c1, c2, c3 = st.columns(3)
    with c1: sal = st.number_input("💵 SALÁRIO BRUTO (R$):", min_value=1.0, value=3000.0)
    with c2: vida = st.number_input("🏠 CUSTO VIDA (R$):", min_value=0.0, value=1500.0)
    with c3: dias = st.number_input("📅 DIAS NO TRECHO:", 1, 31, 22)
    
    st.markdown('<div class="secao-titulo">🚌 LOGÍSTICA DE DESLOCAMENTO</div>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1: p_pub = st.number_input("🚆 PÚBLICO (R$)", 0.0, value=8.80)
    with g2: p_app = st.number_input("📱 APP (R$)", 0.0)
    with g3: p_car = st.number_input("🚗 PRIVADO (R$)", 0.0)
    
    h_trecho = st.slider("⏱️ HORAS NO TRECHO / DIA (TOTAL):", 0.5, 12.0, 3.0, step=0.5)
    btn = st.form_submit_button("PROCESSAR DADOS")

if btn:
    # LÓGICA TÉCNICA
    h_paga_mes = 176
    v_hora_bruta = sal / h_paga_mes
    custo_transp_mes = (p_pub + p_app + p_car) * dias
    h_exprop_mes = h_trecho * dias
    
    # Rendimento Real (Expropriação do Tempo + Custos Diretos)
    v_hora_real = (sal - custo_transp_mes) / (h_paga_mes + h_exprop_mes)
    perda_pct = (1 - (v_hora_real / v_hora_bruta)) * 100
    confisco_monetario = sal * (perda_pct / 100)
    sobra_final = sal - custo_transp_mes - vida
    dias_ano_perdidos = (h_exprop_mes * 12) / 24

    # DASHBOARD DE INDICADORES
    r1, r2, r3 = st.columns(3)
    with r1: st.markdown(f'<div class="card-res"><div class="label-card">RENDIMENTO REAL<br>POR HORA</div><div class="val-res">R$ {v_hora_real:.2f}</div></div>', unsafe_allow_html=True)
    with r2: st.markdown(f'<div class="card-res"><div class="label-card">SALÁRIO REAL<br>CONFISCADO</div><div class="val-res">{perda_pct:.1f}%</div></div>', unsafe_allow_html=True)
    with r3: st.markdown(f'<div class="card-res"><div class="label-card">DIAS DE VIDA<br>NO TRECHO / ANO</div><div class="val-res">{dias_ano_perdidos:.1f}</div></div>', unsafe_allow_html=True)

    # VETOR DE DESLOCAMENTO EM ARCO (PYDECK 3D)
    st.markdown('<div class="secao-titulo">🗺️ VETOR DE FLUXO PENDULAR (GSP)</div>', unsafe_allow_html=True)
    m_lat, m_lon = GEO_SPO[moradia]
    t_lat, t_lon = GEO_SPO[trabalho]

    arc_layer = pdk.Layer(
        "ArcLayer",
        data=[{"s": [m_lon, m_lat], "t": [t_lon, t_lat]}],
        get_source_position="s", get_target_position="t",
        get_source_color=[255, 204, 0, 200], get_target_color=[230, 57, 70, 200],
        get_width=8
    )

    st.pydeck_chart(pdk.Deck(
        map_style=pdk.map_styles.DARK,
        initial_view_state=pdk.ViewState(latitude=(m_lat+t_lat)/2, longitude=(m_lon+t_lon)/2, zoom=9, pitch=45),
        layers=[arc_layer]
    ))

    # SÍNTESE PARA COMUNICAÇÃO PÚBLICA
    st.markdown('<div class="secao-titulo">📝 SÍNTESE PARA COMUNICAÇÃO PÚBLICA</div>', unsafe_allow_html=True)
    sintese = (
        f"ESTUDO DE MOBILIDADE: O trecho {moradia} -> {trabalho} impõe uma expropriação de {perda_pct:.1f}% "
        f"do rendimento real. O trabalhador perde R$ {confisco_monetario:.2f} mensais em tempo e tarifa, "
        f"o que equivale a entregar {dias_ano_perdidos:.1f} dias da sua vida por ano ao deslocamento."
    )
    st.code(sintese, language="text")

    # RELATÓRIO TÉCNICO AVANÇADO
    st.markdown('<div class="secao-titulo">🔬 RELATÓRIO TÉCNICO DE EXPROPRIAÇÃO</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="sintese-box">
            <b>DADOS CONSOLIDADOS:</b><br>
            - Jornada Mensal Expropriada (Trecho): {h_exprop_mes:.1f} horas<br>
            - Custo de Reprodução da Força de Trabalho (Tarifas): R$ {custo_transp_mes:,.2f}<br>
            - Valor Nominal do Salário Confiscado: R$ {confisco_monetario:,.2f}<br>
            - Rendimento Real Líquido (Sobra): R$ {sobra_final:,.2f}<br>
            - Impacto na Hora Bruta (R$ {v_hora_bruta:.2f} → R$ {v_hora_real:.2f})
        </div>
    """, unsafe_allow_html=True)
