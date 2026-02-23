import streamlit as st
import pandas as pd
import pydeck as pdk
from geodata import GEO_SPO 

# 1. ESTILO TERMINAL URBANO (PRETO, AMARELO, VERMELHO)
st.set_page_config(page_title="Beta II - Calculadora do Trecho", layout="centered")

st.markdown("""
    <style>
    /* FUNDO PRINCIPAL */
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    
    /* CHAMADA ALERTA DE EXPROPRIAÇÃO MENSAL */
    .chamada-alerta { 
        background-color: #E63946; color: white; text-align: center; 
        padding: 15px; font-weight: 900; border: 4px solid #FFCC00; 
        margin-bottom: 10px; text-transform: uppercase; font-size: 1.6rem;
    }
    
    /* TÍTULO PRINCIPAL SOLICITADO */
    .titulo-pergunta { 
        color: #FFCC00 !important; font-family: 'Arial Black', sans-serif; 
        font-size: 1.4rem !important; text-align: center; 
        text-transform: uppercase; margin-bottom: 30px; line-height: 1.2;
    }

    /* LABELS EM AMARELO ALTO CONTRASTE */
    label, p, span, .stSelectbox label { 
        color: #FFCC00 !important; 
        font-weight: 800 !important; 
        text-transform: uppercase !important;
        font-size: 1rem !important;
        display: block;
        margin-bottom: 5px;
    }

    .secao-titulo { 
        color: #FFCC00 !important; font-size: 1.2rem !important; font-weight: 800; 
        text-transform: uppercase; margin-top: 30px; border-bottom: 2px solid #FFCC00; padding-bottom: 5px; 
    }

    /* AJUSTE DOS INPUTS PARA CLAREZA E ACESSO */
    .stNumberInput input {
        background-color: #111 !important;
        color: #FFFFFF !important;
        font-size: 1.2rem !important;
        border: 2px solid #FFCC00 !important;
        border-radius: 4px;
        padding: 10px;
    }

    .sintese-box { 
        background-color: #111; border: 2px solid #FFCC00; 
        padding: 20px; margin-top: 20px; color: #FFFFFF; 
        font-family: 'Courier New', monospace; line-height: 1.6; 
    }
    .destaque-amarelo { color: #FFCC00; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

lista_geo = sorted(list(GEO_SPO.keys()))

# 2. CABEÇALHO COM AS CHAMADAS SOLICITADAS
st.markdown('<div class="chamada-alerta">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="titulo-pergunta">Quanto de tempo e de dinheiro são consumidos no seu deslocamento diário?</div>', unsafe_allow_html=True)

# INÍCIO DO FORMULÁRIO (ESTRUTURA SIMPLIFICADA PARA EVITAR TRAVAMENTOS)
with st.form("form_beta_ii"):
    st.markdown('<div class="secao-titulo">🏠 LOCALIZAÇÃO</div>', unsafe_allow_html=True)
    moradia = st.selectbox("ONDE VOCÊ MORA?", lista_geo, index=0)
    trabalho = st.selectbox("ONDE VOCÊ TRABALHA?", lista_geo, index=1)
    
    st.markdown('<div class="secao-titulo">💵 RENDIMENTOS E SOBREVIVÊNCIA</div>', unsafe_allow_html=True)
    sal_bruto = st.number_input("SALÁRIO BRUTO MENSAL (R$):", min_value=1.0, value=3000.0, step=100.0)
    custo_vida = st.number_input("CUSTO DE VIDA FIXO (R$):", min_value=0.0, value=1500.0, step=50.0, 
                                 help="OPCIONAL: Aluguel, contas e alimentação. Este valor não altera o valor da hora, apenas a sobra final.") #
    
    st.markdown('<div class="secao-titulo">🚌 CUSTOS NO TRECHO (DIÁRIO IDA+VOLTA)</div>', unsafe_allow_html=True)
    p_pub = st.number_input("🚆 ÔNIBUS / METRÔ / TREM (R$):", min_value=0.0, value=8.80)
    p_app = st.number_input("📱 APP / TÁXI (R$):", min_value=0.0, value=0.0)
    p_car = st.number_input("🚗 CARRO / MOTO (R$):", min_value=0.0, value=0.0)
    
    st.write("")
    dias_mes = st.number_input("DIAS DE DESLOCAMENTO POR MÊS:", 1, 31, 22)
    
    st.markdown('<div class="secao-titulo">⏱️ TEMPO DE EXPROPRIAÇÃO</div>', unsafe_allow_html=True)
    h_trecho_dia = st.slider("TOTAL DE HORAS NO TRECHO POR DIA (IDA+VOLTA):", 0.5, 12.0, 3.0, step=0.5)
    
    # BOTÃO DE SUBMISSÃO (MUITO IMPORTANTE)
    btn = st.form_submit_button("EFETUAR CÁLCULO DE IMPACTO")

if btn:
    # LÓGICA TÉCNICA DINÂMICA
    h_pagas_mes = 176
    custo_transp_mes = (p_pub + p_app + p_car) * dias_mes
    h_exprop_mes = h_trecho_dia * dias_mes
    
    # Rendimento Real: (Salário - Custo Transp) / (Horas Pagas + Horas Trecho)
    v_hora_nominal = sal_bruto / h_pagas_mes
    v_hora_real = (sal_bruto - custo_transp_mes) / (h_pagas_mes + h_exprop_mes)
    
    depreciacao_pct = (1 - (v_hora_real / v_hora_nominal)) * 100
    salario_confiscado = sal_bruto * (depreciacao_pct / 100)
    
    # Custo de vida afeta apenas a Sobra Final (Rendimento Residual)
    rendimento_residual = sal_bruto - custo_transp_mes - custo_vida
    dias_vida_ano = (h_exprop_mes * 12) / 24

    # MAPA (VETOR PENDULAR ROAD STYLE)
    st.markdown('<div class="secao-titulo">🗺️ VETOR DE FLUXO PENDULAR</div>', unsafe_allow_html=True)
    m_lat, m_lon = GEO_SPO[moradia]
    t_lat, t_lon = GEO_SPO[trabalho]
    
    st.pydeck_chart(pdk.Deck(
        map_style=pdk.map_styles.ROAD,
        initial_view_state=pdk.ViewState(latitude=(m_lat+t_lat)/2, longitude=(m_lon+t_lon)/2, zoom=10, pitch=45),
        layers=[pdk.Layer("ArcLayer", data=[{"s": [m_lon, m_lat], "t": [t_lon, t_lat]}], 
                get_source_position="s", get_target_position="t", 
                get_color=[230, 57, 70, 200], get_width=12)]
    ))

    # SÍNTESE E RELATÓRIO
    st.markdown('<div class="secao-titulo">📝 SÍNTESE PARA COMUNICAÇÃO PÚBLICA</div>', unsafe_allow_html=True)
    sintese_txt = (f"MOBILIDADE GSP: O trajeto {moradia}-{trabalho} confisca {depreciacao_pct:.1f}% do rendimento real. "
                   f"O valor da hora cai para R$ {v_hora_real:.2f}, resultando em {dias_vida_ano:.1f} dias perdidos/ano.")
    st.code(sintese_txt, language="text")

    st.markdown('<div class="secao-titulo">🔬 MÉTRICAS CONSOLIDADAS DE EXPROPRIAÇÃO</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="sintese-box">
            • <span class="destaque-amarelo">TEMPO MENSAL EXPROPRIADO:</span> {h_exprop_mes:.1f}h<br>
            • <span class="destaque-amarelo">CUSTO DE REPRODUÇÃO (TARIFAS):</span> R$ {custo_transp_mes:,.2f}<br>
            • <span class="destaque-amarelo">VALOR NOMINAL DO CONFISCO:</span> R$ {salario_confiscado:,.2f}<br>
            • <span class="destaque-amarelo">RENDIMENTO RESIDUAL (SOBRA FINAL):</span> R$ {rendimento_residual:,.2f}<br>
            • <span class="destaque-amarelo">DEPRECIAÇÃO DA HORA DE TRABALHO:</span> {depreciacao_pct:.1f}%
        </div>
    """, unsafe_allow_html=True)
