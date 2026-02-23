import streamlit as st
import pandas as pd
from geodata import GEO_SPO 

# 1. ESTILO TERMINAL URBANO REFINADO
st.set_page_config(page_title="Beta II - Calculadora do Trecho", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    
    /* TITULOS E LABELS EM AMARELO */
    label, .stSelectbox label { 
        color: #FFCC00 !important; 
        font-weight: 800 !important; 
        text-transform: uppercase !important;
        font-size: 1rem !important;
    }
    
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

    /* CORREÇÃO DOS INPUTS: REMOÇÃO DE SOBREPOSIÇÃO PARA TORNAR EDITÁVEL */
    .stNumberInput div[data-baseweb="input"] {
        background-color: #111 !important;
    }
    .stNumberInput input {
        color: #FFFFFF !important;
        font-size: 1.2rem !important;
    }

    /* SÍNTESE COMPACTA E INTEGRAL */
    .sintese-box { 
        background-color: #111; border: 2px solid #FFCC00; 
        padding: 15px; margin-top: 10px; color: #FFFFFF; 
        font-family: 'Arial', sans-serif; font-size: 1rem; 
        line-height: 1.4; word-wrap: break-word;
    }
    
    /* VETOR DE IMPACTO (ALTERNATIVA AO MAPA) */
    .vetor-container {
        display: flex; align-items: center; justify-content: space-between;
        padding: 20px; background: #111; border-radius: 8px; margin-top: 10px;
        border: 1px border: 1px solid #333;
    }
    .ponto { text-align: center; flex: 1; }
    .seta { flex: 2; text-align: center; color: #E63946; font-size: 2rem; font-weight: bold; }
    .label-local { color: #FFCC00; font-weight: bold; font-size: 0.9rem; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

lista_geo = sorted(list(GEO_SPO.keys()))

st.markdown('<div class="chamada-alerta">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="titulo-pergunta">Quanto de tempo e de dinheiro são consumidos no seu deslocamento diário?</div>', unsafe_allow_html=True)

with st.form("beta_ii_v12"):
    c_geo1, c_geo2 = st.columns(2)
    with c_geo1: moradia = st.selectbox("🏠 ORIGEM (MORADIA):", lista_geo, index=0)
    with c_geo2: trabalho = st.selectbox("💼 DESTINO (TRABALHO):", lista_geo, index=1)
    
    st.markdown('<div class="secao-titulo">💵 RENDIMENTOS E SOBREVIVÊNCIA</div>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    with r1: sal_bruto = st.number_input("SALÁRIO BRUTO MENSAL (R$):", min_value=0.0, value=3000.0, step=100.0)
    with r2: custo_vida = st.number_input("CUSTO DE VIDA FIXO (R$):", min_value=0.0, value=1500.0, step=50.0, help="Preenchimento opcional (Aluguel, Contas, Comida).")
    
    st.markdown('<div class="secao-titulo">🚌 CUSTOS NO TRECHO (ÔNIBUS/METRÔ/APP/CARRO)</div>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1: p_pub = st.number_input("🚆 TRANSP. PÚBLICO (R$):", min_value=0.0, value=8.80)
    with g2: p_app = st.number_input("📱 APP/TÁXI (R$):", min_value=0.0)
    with g3: p_car = st.number_input("🚗 CARRO/COMBUST. (R$):", min_value=0.0)
    
    d3, d4 = st.columns(2)
    with d3: dias_mes = st.number_input("DIAS NO TRECHO / MÊS:", 1, 31, 22)
    with d4: h_trecho = st.slider("HORAS NO TRECHO / DIA (TOTAL):", 0.5, 12.0, 3.0, step=0.5)
    
    btn = st.form_submit_button("PROCESSAR IMPACTO REAL")

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

    # ALTERNATIVA AO MAPA: VETOR DE FLUXO PENDULAR
    st.markdown('<div class="secao-titulo">🗺️ VETOR DE DESLOCAMENTO PENDULAR</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="vetor-container">
            <div class="ponto"><span class="label-local">{moradia}</span><br>🏠 ORIGEM</div>
            <div class="seta">――――▶</div>
            <div class="ponto"><span class="label-local">{trabalho}</span><br>💼 DESTINO</div>
        </div>
    """, unsafe_allow_html=True)

    # SÍNTESE COMPACTA E INTEGRAL
    st.markdown('<div class="secao-titulo">📝 SÍNTESE PARA COMUNICAÇÃO PÚBLICA</div>', unsafe_allow_html=True)
    sintese_txt = (f"MOBILIDADE GSP: O trajeto {moradia}-{trabalho} confisca {depreciacao_pct:.1f}% do rendimento real. "
                   f"O valor da hora cai para R$ {v_hora_real:.2f}, resultando em {dias_vida_ano:.1f} dias perdidos/ano.")
    st.markdown(f'<div class="sintese-box">{sintese_txt}</div>', unsafe_allow_html=True)

    # MÉTRICAS CONSOLIDADAS (O COMPARATIVO ANTES VS DEPOIS)
    st.markdown('<div class="secao-titulo">🔬 MÉTRICAS CONSOLIDADAS DE EXPROPRIAÇÃO</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="sintese-box">
            • <b>VALOR DA HORA:</b> De <span style="color:#FFF">R$ {v_hora_nominal:.2f}</span> para <span style="color:#E63946">R$ {v_hora_real:.2f}</span><br>
            • <b>TEMPO MENSAL EXPROPRIADO:</b> <span style="color:#FFCC00">{h_exprop_mes:.1f}h</span><br>
            • <b>CUSTO DE REPRODUÇÃO (TARIFAS):</b> <span style="color:#FFCC00">R$ {custo_transp_mes:,.2f}</span><br>
            • <b>VALOR NOMINAL DO CONFISCO:</b> <span style="color:#E63946">R$ {salario_confiscado:,.2f}</span><br>
            • <b>RENDIMENTO RESIDUAL (SOBRA FINAL):</b> <span style="color:#FFCC00">R$ {rendimento_residual:,.2f}</span><br>
            • <b>DEPRECIAÇÃO REAL DA HORA:</b> <span style="color:#E63946">{depreciacao_pct:.1f}%</span>
        </div>
    """, unsafe_allow_html=True)
