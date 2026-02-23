import streamlit as st
import pandas as pd
from geodata import GEO_SPO 

# 1. ESTILO TERMINAL DE DADOS (PRETO/AMARELO/VERMELHO)
st.set_page_config(page_title="Beta II - Calculadora do Trecho", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    
    label, .stSelectbox label, .stNumberInput label { 
        color: #FFCC00 !important; font-weight: 800 !important; 
        text-transform: uppercase !important; font-size: 0.9rem !important;
    }

    .chamada-alerta { 
        background-color: #E63946; color: white; text-align: center; 
        padding: 10px; font-weight: 900; border: 2px solid #FFCC00; 
        margin-bottom: 8px; text-transform: uppercase; font-size: 1.2rem;
    }
    
    .titulo-pergunta { 
        color: #FFCC00 !important; font-family: 'Arial', sans-serif; 
        font-size: 1.1rem !important; text-align: center; 
        text-transform: uppercase; margin-bottom: 25px; font-weight: 700;
    }

    .secao-titulo { 
        color: #FFCC00 !important; font-size: 1rem !important; font-weight: 800; 
        text-transform: uppercase; margin-top: 25px; border-bottom: 1px solid #FFCC00; padding-bottom: 3px; 
    }

    .stNumberInput input { background-color: #111 !important; color: #FFFFFF !important; font-size: 1.1rem !important; border: 1px solid #333 !important; }

    .sintese-box { 
        background-color: #111; border: 1px solid #FFCC00; 
        padding: 18px; margin-top: 10px; color: #FFFFFF; 
        font-family: 'Courier New', monospace; font-size: 1rem; line-height: 1.4;
    }
    
    .expro-destaque { color: #E63946; font-weight: 900; }
    .valor-amarelo { color: #FFCC00; font-weight: bold; }
    
    /* ESTILO DO BOTÃO DE AJUDA ? */
    .stTooltipIcon { color: #E63946 !important; font-size: 1.2rem !important; }
    </style>
    """, unsafe_allow_html=True)

lista_geo = sorted(list(GEO_SPO.keys()))

st.markdown('<div class="chamada-alerta">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="titulo-pergunta">Quanto de tempo e de dinheiro são consumidos no seu deslocamento diário?</div>', unsafe_allow_html=True)

with st.form("beta_ii_v17"):
    st.markdown('<div class="secao-titulo">📍 GEOGRAFIA DO FLUXO</div>', unsafe_allow_html=True)
    c_geo1, c_geo2 = st.columns(2)
    with c_geo1: moradia = st.selectbox("MORADIA (ORIGEM):", lista_geo, index=0)
    with c_geo2: trabalho = st.selectbox("TRABALHO (DESTINO):", lista_geo, index=1)
    
    st.markdown('<div class="secao-titulo">💵 RENDIMENTOS E SOBREVIVÊNCIA</div>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    with r1: sal_bruto = st.number_input("SALÁRIO BRUTO (R$):", min_value=0.0, step=100.0, value=3000.0)
    with r2: custo_vida = st.number_input("CUSTO DE VIDA FIXO (R$):", min_value=0.0, step=50.0, value=1500.0,
                                         help="ESTE CAMPO É OPCIONAL. Inclua aqui gastos com Aluguel, Alimentação, Luz e Internet. Este valor NÃO altera o valor da sua hora trabalhada, apenas demonstra a sobra final após custos de sobrevivência.")
    
    st.markdown('<div class="secao-titulo">🚌 CUSTOS NO TRECHO (ÔNIBUS/METRÔ/TREM/APP/CARRO)</div>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1: p_pub = st.number_input("🚆 TRANSP. PÚBLICO", min_value=0.0, value=8.80)
    with g2: p_app = st.number_input("📱 APP/TÁXI", min_value=0.0)
    with g3: p_car = st.number_input("🚗 CARRO/COMBUSTÍVEL", min_value=0.0)
    
    dias_m = st.number_input("DIAS DE DESLOCAMENTO NO MÊS:", 1, 31, 22)
    h_dia = st.slider("HORAS NO TRECHO POR DIA (TOTAL):", 0.5, 12.0, 3.0, step=0.5)
    
    submit = st.form_submit_button("PROCESSAR DADOS DE IMPACTO")

if submit:
    # LÓGICA TÉCNICA
    h_pagas = 176
    v_hora_nom = sal_bruto / h_pagas if sal_bruto > 0 else 0
    custo_transp_mensal = (p_pub + p_app + p_car) * dias_m
    h_trecho_mensal = h_dia * dias_m
    
    # Rendimento Real: (Salário - Tarifas) / (Horas Pagas + Horas Trecho)
    v_hora_real = (sal_bruto - custo_transp_mensal) / (h_pagas + h_trecho_mensal) if sal_bruto > 0 else 0
    perda_p = (1 - (v_hora_real / v_hora_nom)) * 100 if v_hora_nom > 0 else 0
    
    # Confisco Nominal = Gastos com Transporte + (Horas de Trecho x Valor da Hora Nominal)
    valor_tempo_expro = h_trecho_mensal * v_hora_nom
    confisco_monetario = custo_transp_mensal + valor_tempo_expro
    
    sobra = sal_bruto - custo_transp_mensal - custo_vida

    # VETOR DE FLUXO
    st.markdown('<div class="secao-titulo">🗺️ VETOR DE DESLOCAMENTO PENDULAR</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div style="background: #111; padding: 20px; border: 1px solid #333; text-align: center;">
            <span style="color:#FFCC00; font-weight:bold;">🏠 {moradia}</span>
            <span style="color:#E63946; font-size:1.5rem; margin: 0 15px;">⚡――――▶</span>
            <span style="color:#FFCC00; font-weight:bold;">💼 {trabalho}</span>
            <p style="color:#E63946; font-size:0.8rem; margin-top:10px; font-weight:bold;">O DESLOCAMENTO CASA-TRABALHO É TEMPO DE TRABALHO NÃO PAGO</p>
        </div>
    """, unsafe_allow_html=True)

    # SÍNTESE
    st.markdown('<div class="secao-titulo">📝 SÍNTESE PARA COMUNICAÇÃO PÚBLICA</div>', unsafe_allow_html=True)
    sintese_txt = (f"MOBILIDADE GSP: O trajeto {moradia}-{trabalho} confisca {perda_p:.1f}% do rendimento real. "
                   f"O valor da hora cai de R$ {v_hora_nom:.2f} para R$ {v_hora_real:.2f}, resultando em {h_trecho_mensal:.1f} horas não pagas por mês.")
    st.markdown(f'<div class="sintese-box">{sintese_txt}</div>', unsafe_allow_html=True)

    # MÉTRICAS CONSOLIDADAS
    st.markdown('<div class="secao-titulo">🔬 MÉTRICAS CONSOLIDADAS DE EXPROPRIAÇÃO</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="sintese-box">
            • <span class="valor-amarelo">RENDIMENTO POR HORA:</span> De R$ {v_hora_nom:.2f} para <span class="expro-destaque">R$ {v_hora_real:.2f}</span><br>
            • <span class="expro-destaque">HORAS DE TRABALHO NÃO PAGAS:</span> {h_trecho_mensal:.1f}h/mês<br>
            • <span class="valor-amarelo">VALOR NOMINAL DO CONFISCO:</span> R$ {confisco_monetario:,.2f}<br>
            • <span class="valor-amarelo">RENDIMENTO RESIDUAL (SOBRA):</span> R$ {sobra:,.2f}<br>
            • <span class="expro-destaque">DEPRECIAÇÃO DA FORÇA DE TRABALHO:</span> {perda_p:.1f}%
        </div>
    """, unsafe_allow_html=True)
