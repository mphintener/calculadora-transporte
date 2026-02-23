import streamlit as st
import pandas as pd
from geodata import GEO_SPO 

# 1. IDENTIDADE VISUAL DE ALTO CONTRASTE (PRETO, AMARELO, VERMELHO)
st.set_page_config(page_title="Beta II - Calculadora do Trecho", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    
    label, .stSelectbox label, .stNumberInput label { 
        color: #FFCC00 !important; font-weight: 800 !important; 
        text-transform: uppercase !important; font-size: 1.1rem !important;
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

    /* INPUTS EDITÁVEIS E NÍTIDOS */
    .stNumberInput input { 
        background-color: #111 !important; color: #FFFFFF !important; 
        font-size: 1.2rem !important; border: 1px solid #FFCC00 !important; 
    }

    .sintese-box { 
        background-color: #111; border: 2px solid #FFCC00; 
        padding: 20px; margin-top: 10px; color: #FFFFFF; 
        font-family: 'Courier New', monospace; font-size: 1.1rem; line-height: 1.5;
    }
    
    .expro-destaque { color: #E63946; font-weight: 900; }
    .valor-amarelo { color: #FFCC00; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

lista_geo = sorted(list(GEO_SPO.keys()))

st.markdown('<div class="chamada-alerta">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="titulo-pergunta">Quanto de tempo e de dinheiro são consumidos no seu deslocamento diário?</div>', unsafe_allow_html=True)

with st.form("form_beta_ii_final_v2"):
    st.markdown('<h4 style="color:#FFCC00">🏠 GEOGRAFIA DO TRECHO</h4>', unsafe_allow_html=True)
    c_geo1, c_geo2 = st.columns(2)
    with c_geo1: moradia = st.selectbox("ORIGEM (MORADIA):", lista_geo, index=0)
    with c_geo2: trabalho = st.selectbox("DESTINO (TRABALHO):", lista_geo, index=1)
    
    st.markdown('<h4 style="color:#FFCC00">💵 RENDIMENTOS E SOBREVIVÊNCIA</h4>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    with r1: sal_bruto = st.number_input("SALÁRIO BRUTO (R$):", min_value=0.0, value=3000.0)
    with r2: custo_v = st.number_input("CUSTO DE VIDA FIXO (R$):", min_value=0.0, value=1500.0, 
                                      help="OPCIONAL: Aluguel, comida e contas. Não altera o valor da hora técnica.")
    
    st.markdown('<h4 style="color:#FFCC00">🚌 CUSTOS NO TRECHO (DIÁRIO IDA+VOLTA)</h4>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1: p_pub = st.number_input("🚆 ÔNIBUS/METRÔ/TREM:", min_value=0.0, value=8.80)
    with g2: p_app = st.number_input("📱 APP/TÁXI:", min_value=0.0)
    with g3: p_car = st.number_input("🚗 CARRO/COMBUSTÍVEL:", min_value=0.0)
    
    dias_m = st.number_input("DIAS DE TRECHO NO MÊS:", 1, 31, 22)
    h_dia = st.slider("TOTAL DE HORAS NO TRECHO / DIA:", 0.5, 12.0, 3.0, step=0.5)
    
    submit = st.form_submit_button("ANALISAR EXPROPRIAÇÃO")

if submit:
    # LÓGICA TÉCNICA
    h_pagas = 176
    custo_transp_mensal = (p_pub + p_app + p_car) * dias_m
    h_exprop_mensal = h_dia * dias_m
    
    v_hora_nom = sal_bruto / h_pagas
    # Valor Real da Hora: Salário descontando transporte, dividido por horas pagas + horas de trecho
    v_hora_real = (sal_bruto - custo_transp_mensal) / (h_pagas + h_exprop_mensal)
    
    depreciacao_p = (1 - (v_hora_real / v_hora_nom)) * 100
    # Confisco Nominal: Gastos diretos + Valor das horas de vida transformadas em trabalho não pago
    valor_tempo_expropriado = h_exprop_mensal * v_hora_nom
    confisco_nominal = custo_transp_mensal + valor_tempo_expropriado
    
    rendimento_residual = sal_bruto - custo_transp_mensal - custo_v
    dias_ano_no_trecho = (h_exprop_mensal * 12) / 24

    # VETOR DE FLUXO PENDULAR (ALTO IMPACTO VISUAL)
    st.markdown('<h4 style="color:#FFCC00">🗺️ VETOR DE FLUXO PENDULAR</h4>', unsafe_allow_html=True)
    st.markdown(f"""
        <div style="background: #111; padding: 25px; border: 1px solid #E63946; text-align: center;">
            <span style="color:#FFCC00; font-family:'Arial Black'; font-size:1.2rem;">🏠 {moradia}</span>
            <span style="color:#E63946; font-size:2rem; margin: 0 20px;">⚡――――▶</span>
            <span style="color:#FFCC00; font-family:'Arial Black'; font-size:1.2rem;">💼 {trabalho}</span>
            <p style="color:#E63946; margin-top:10px; font-weight:bold;">DESLOCAMENTO É TEMPO DE TRABALHO NÃO PAGO</p>
        </div>
    """, unsafe_allow_html=True)

    # SÍNTESE COMPACTA PARA COMUNICAÇÃO PÚBLICA
    st.markdown('<h4 style="color:#FFCC00">📝 SÍNTESE DA EXPROPRIAÇÃO</h4>', unsafe_allow_html=True)
    sintese_txt = (f"MOBILIDADE GSP: O trajeto {moradia}-{trabalho} confisca {depreciacao_p:.1f}% do rendimento real. "
                   f"O valor da hora cai para R$ {v_hora_real:.2f}, resultando em {h_exprop_mensal:.1f} HORAS NÃO PAGAS por mês.")
    st.markdown(f'<div class="sintese-box">{sintese_txt}</div>', unsafe_allow_html=True)

    # MÉTRICAS CONSOLIDADAS
    st.markdown('<h4 style="color:#FFCC00">🔬 MÉTRICAS CONSOLIDADAS</h4>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="sintese-box">
            • <span class="expro-destaque">VALOR DA HORA:</span> De R$ {v_hora_nom:.2f} para <span class="expro-destaque">R$ {v_hora_real:.2f}</span><br>
            • <span class="expro-destaque">HORAS DE TRABALHO NÃO PAGAS:</span> {h_exprop_mensal:.1f}h/mês<br>
            • <span class="valor-amarelo">VALOR NOMINAL DO CONFISCO:</span> R$ {confisco_nominal:.2f}<br>
            • <span class="valor-amarelo">RENDIMENTO RESIDUAL (SOBRA FINAL):</span> R$ {rendimento_residual:.2f}<br>
            • <span class="expro-destaque">DEPRECIAÇÃO DA FORÇA DE TRABALHO:</span> {depreciacao_p:.1f}%
        </div>
    """, unsafe_allow_html=True)
