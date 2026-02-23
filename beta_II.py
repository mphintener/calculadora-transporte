import streamlit as st
import pandas as pd
from geodata import GEO_SPO 

# 1. ESTILO ALTO CONTRASTE (TERMINAL URBANO)
st.set_page_config(page_title="Beta II - Calculadora do Trecho", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    
    /* TITULOS EM AMARELO */
    label, .stSelectbox label, .stNumberInput label { 
        color: #FFCC00 !important; 
        font-weight: 800 !important; 
        text-transform: uppercase !important;
        font-size: 1.1rem !important;
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

    /* QUADROS DE RESULTADO */
    .sintese-box { 
        background-color: #111; border: 2px solid #FFCC00; 
        padding: 20px; margin-top: 10px; color: #FFFFFF; 
        font-family: 'Arial', sans-serif; font-size: 1.1rem; line-height: 1.5;
    }
    
    .destaque-vermelho { color: #E63946; font-weight: 900; }
    .destaque-amarelo { color: #FFCC00; font-weight: bold; }
    
    /* VETOR DE FLUXO */
    .vetor-fluxo {
        display: flex; align-items: center; justify-content: space-around;
        background: #111; padding: 25px; border-radius: 10px; border: 1px solid #E63946;
        margin-top: 20px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

lista_geo = sorted(list(GEO_SPO.keys()))

st.markdown('<div class="chamada-alerta">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="titulo-pergunta">Quanto de tempo e de dinheiro são consumidos no seu deslocamento diário?</div>', unsafe_allow_html=True)

# INÍCIO DO FORMULÁRIO COM CAMPOS DESTRAVADOS
with st.form("beta_ii_v15"):
    st.markdown('<h4 style="color:#FFCC00">🏠 GEOGRAFIA DO FLUXO</h4>', unsafe_allow_html=True)
    moradia = st.selectbox("ORIGEM (MORADIA):", lista_geo, index=0)
    trabalho = st.selectbox("DESTINO (TRABALHO):", lista_geo, index=1)
    
    st.markdown('<h4 style="color:#FFCC00">💵 RENDIMENTOS E SOBREVIVÊNCIA</h4>', unsafe_allow_html=True)
    sal_bruto = st.number_input("SALÁRIO BRUTO MENSAL (R$):", min_value=0.0, step=100.0, key="sal")
    custo_vida = st.number_input("CUSTO DE VIDA FIXO (R$):", min_value=0.0, step=50.0, key="vida",
                                 help="Opcional: Aluguel, mercado, contas. Não altera o valor da hora técnica.")
    
    st.markdown('<h4 style="color:#FFCC00">🚌 CUSTOS NO TRECHO (DIÁRIO IDA+VOLTA)</h4>', unsafe_allow_html=True)
    p_pub = st.number_input("🚆 ÔNIBUS / METRÔ / TREM (R$):", min_value=0.0, step=0.10)
    p_app = st.number_input("📱 APP / TÁXI (R$):", min_value=0.0, step=1.0)
    p_car = st.number_input("🚗 CARRO / COMBUSTÍVEL (R$):", min_value=0.0, step=1.0)
    
    st.write("")
    dias_m = st.number_input("DIAS DE DESLOCAMENTO NO MÊS:", min_value=1, max_value=31, value=22)
    h_dia = st.slider("TOTAL DE HORAS NO TRECHO (DIA):", 0.5, 12.0, 3.0, step=0.5)
    
    submit = st.form_submit_button("PROCESSAR DADOS DE EXPROPRIAÇÃO")

if submit:
    # LÓGICA TÉCNICA DINÂMICA
    h_pagas = 176
    v_hora_nom = sal_bruto / h_pagas if sal_bruto > 0 else 0
    custo_transp_total = (p_pub + p_app + p_car) * dias_m
    h_trecho_total = h_dia * dias_m
    
    # Rendimento Real corrigido: Salário - Tarifas / Horas Totais
    v_hora_real = (sal_bruto - custo_transp_total) / (h_pagas + h_trecho_total) if sal_bruto > 0 else 0
    perda_p = (1 - (v_hora_real / v_hora_nom)) * 100 if v_hora_nom > 0 else 0
    sal_confiscado = sal_bruto * (perda_p / 100)
    sobra = sal_bruto - custo_transp_total - custo_vida

    # VETOR DE IMPACTO (O MAPA ACABOU)
    st.markdown('<h4 style="color:#FFCC00">🗺️ VETOR DE DESLOCAMENTO PENDULAR</h4>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="vetor-fluxo">
            <div><span style="color:#FFCC00; font-size:1.3rem; font-weight:bold;">🏠 {moradia}</span></div>
            <div style="color:#E63946; font-size:2rem;">⚡――――▶</div>
            <div><span style="color:#FFCC00; font-size:1.3rem; font-weight:bold;">💼 {trabalho}</span></div>
        </div>
        <p style="text-align:center; color:#E63946; font-weight:bold; margin-top:10px;">
            O DESLOCAMENTO É TEMPO DE TRABALHO NÃO PAGO.
        </p>
    """, unsafe_allow_html=True)

    # SÍNTESE COMPACTA PARA COMUNICAÇÃO PÚBLICA
    st.markdown('<h4 style="color:#FFCC00">📝 SÍNTESE DA EXPROPRIAÇÃO</h4>', unsafe_allow_html=True)
    sintese_txt = (f"MOBILIDADE GSP: O trajeto {moradia}-{trabalho} confisca {perda_p:.1f}% do rendimento real. "
                   f"O valor da hora cai para R$ {v_hora_real:.2f}, resultando em {h_trecho_total:.1f} horas não pagas por mês.")
    st.markdown(f'<div class="sintese-box">{sintese_txt}</div>', unsafe_allow_html=True)

    # MÉTRICAS CONSOLIDADAS
    st.markdown('<h4 style="color:#FFCC00">🔬 MÉTRICAS CONSOLIDADAS</h4>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="sintese-box">
            • <span class="destaque-vermelho">VALOR DA HORA TRABALHADA:</span> De R$ {v_hora_nom:.2f} para <span class="destaque-vermelho">R$ {v_hora_real:.2f}</span><br>
            • <span class="destaque-amarelo">HORAS DE TRABALHO NÃO PAGAS:</span> {h_trecho_total:.1f}h/mês<br>
            • <span class="destaque-amarelo">VALOR NOMINAL DO CONFISCO:</span> R$ {sal_confiscado:,.2f}<br>
            • <span class="destaque-amarelo">RENDIMENTO RESIDUAL (SOBRA FINAL):</span> R$ {sobra:,.2f}<br>
            • <span class="destaque-vermelho">DEPRECIAÇÃO DA FORÇA DE TRABALHO:</span> {perda_p:.1f}%
        </div>
    """, unsafe_allow_html=True)
