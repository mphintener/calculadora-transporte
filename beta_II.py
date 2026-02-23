import streamlit as st
import pandas as pd
from geodata import GEO_SPO 

# 1. IDENTIDADE VISUAL: TERMINAL DE DADOS (PRETO/AMARELO/VERMELHO)
st.set_page_config(page_title="Beta II - Calculadora do Trecho", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    
    /* TITULOS E LABELS */
    label, .stSelectbox label, .stNumberInput label { 
        color: #FFCC00 !important; font-weight: 800 !important; 
        text-transform: uppercase !important; font-size: 0.85rem !important;
    }

    .chamada-alerta { 
        background-color: #E63946; color: white; text-align: center; 
        padding: 10px; font-weight: 900; border: 2px solid #FFCC00; 
        margin-bottom: 8px; text-transform: uppercase; font-size: 1.1rem;
    }
    
    .titulo-pergunta { 
        color: #FFCC00 !important; font-family: 'Arial', sans-serif; 
        font-size: 1rem !important; text-align: center; 
        text-transform: uppercase; margin-bottom: 25px;
    }

    /* INPUTS TOTALMENTE EDITÁVEIS */
    .stNumberInput input { background-color: #111 !important; color: #FFFFFF !important; font-size: 1.1rem !important; border: 1px solid #444 !important; }

    .sintese-box { 
        background-color: #111; border: 1px solid #FFCC00; 
        padding: 18px; margin-top: 10px; color: #FFFFFF; 
        font-family: 'Courier New', monospace; font-size: 1rem;
    }
    
    .expro-destaque { color: #E63946; font-weight: 900; }
    .valor-amarelo { color: #FFCC00; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

lista_geo = sorted(list(GEO_SPO.keys()))

st.markdown('<div class="chamada-alerta">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="titulo-pergunta">Quanto de tempo e de dinheiro são consumidos no seu deslocamento diário?</div>', unsafe_allow_html=True)

with st.form("form_beta_ii_final_v3"):
    st.markdown('<h4 style="color:#FFCC00; font-size:1rem;">📍 GEOGRAFIA DO FLUXO</h4>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: moradia = st.selectbox("MORADIA (ORIGEM):", lista_geo, index=0)
    with c2: trabalho = st.selectbox("TRABALHO (DESTINO):", lista_geo, index=1)
    
    st.markdown('<h4 style="color:#FFCC00; font-size:1rem;">💵 RENDIMENTOS E SOBREVIVÊNCIA</h4>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    with r1: sal_bruto = st.number_input("SALÁRIO BRUTO (R$):", min_value=0.0, step=100.0, value=3000.0)
    with r2: custo_vida = st.number_input("CUSTO DE VIDA FIXO (R$):", min_value=0.0, step=50.0, value=1500.0, help="OPCIONAL. Aluguel, comida e contas. Não altera o valor da hora.")
    
    st.markdown('<h4 style="color:#FFCC00; font-size:1rem;">🚌 CUSTOS NO TRECHO (ÔNIBUS/METRÔ/TREM/APP/CARRO)</h4>', unsafe_allow_html=True)
    p_diario = st.number_input("GASTO DIÁRIO TOTAL (IDA+VOLTA):", min_value=0.0, value=8.80)
    
    col_d, col_h = st.columns(2)
    with col_d: dias_m = st.number_input("DIAS DE TRECHO NO MÊS:", 1, 31, 22)
    with col_h: h_dia = st.slider("TOTAL DE HORAS NO TRECHO / DIA:", 0.5, 12.0, 3.0, step=0.5)
    
    submit = st.form_submit_button("PROCESSAR IMPACTO REAL")

if submit:
    # LÓGICA TÉCNICA REFINADA
    h_pagas = 176
    v_hora_nom = sal_bruto / h_pagas if sal_bruto > 0 else 0
    custo_transp_mensal = p_diario * dias_m
    h_trecho_mensal = h_dia * dias_m
    
    # CONFISCO NOMINAL: (Horas no Trecho * Valor Hora Nominal) + Gasto Transporte
    confisco_total = (h_trecho_mensal * v_hora_nom) + custo_transp_mensal
    
    # VALOR REAL DA HORA: (Salário - Transporte) / (Horas Pagas + Horas Trecho)
    v_hora_real = (sal_bruto - custo_transp_mensal) / (h_pagas + h_trecho_mensal) if sal_bruto > 0 else 0
    
    depreciacao_p = (1 - (v_hora_real / v_hora_nom)) * 100 if v_hora_nom > 0 else 0
    sobra_residual = sal_bruto - custo_transp_mensal - custo_vida

    # VETOR DE FLUXO PENDULAR DETALHADO (SUBSTITUTO DO MAPA)
    st.markdown('<h4 style="color:#FFCC00; font-size:1rem;">🗺️ VETOR DE DESLOCAMENTO PENDULAR</h4>', unsafe_allow_html=True)
    st.markdown(f"""
        <div style="background: #111; padding: 25px; border: 1px solid #E63946; text-align: center;">
            <div style="display: flex; justify-content: space-around; align-items: center;">
                <div style="color: #FFCC00;"><b>🏠 {moradia}</b><br><small>{h_dia/2}h (IDA)</small></div>
                <div style="color: #E63946; font-size: 1.5rem;">⚡――――▶</div>
                <div style="color: #FFCC00;"><b>💼 {trabalho}</b><br><small>{h_dia/2}h (VOLTA)</small></div>
            </div>
            <p style="color:#E63946; font-size:0.85rem; margin-top:15px; font-weight:bold; border-top: 1px solid #333; padding-top:10px;">
                O DESLOCAMENTO É TEMPO DE TRABALHO NÃO PAGO
            </p>
        </div>
    """, unsafe_allow_html=True)

    # SÍNTESE
    st.markdown('<h4 style="color:#FFCC00; font-size:1rem;">📝 SÍNTESE DA EXPROPRIAÇÃO</h4>', unsafe_allow_html=True)
    sintese_txt = (f"Ao se deslocar entre {moradia} e {trabalho}, você dedica {h_trecho_mensal:.1f}h "
                   f"não remuneradas por mês. O valor da hora real cai para R$ {v_hora_real:.2f}.")
    st.markdown(f'<div class="sintese-box">{sintese_txt}</div>', unsafe_allow_html=True)

    # MÉTRICAS CONSOLIDADAS
    st.markdown('<h4 style="color:#FFCC00; font-size:1rem;">🔬 MÉTRICAS CONSOLIDADAS</h4>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="sintese-box">
            • <span class="valor-amarelo">RENDIMENTO POR HORA:</span> De R$ {v_hora_nom:.2f} para <span class="expro-destaque">R$ {v_hora_real:.2f}</span><br>
            • <span class="expro-destaque">HORAS DE TRABALHO NÃO PAGAS:</span> {h_trecho_mensal:.1f}h/mês<br>
            • <span class="valor-amarelo">VALOR NOMINAL DO CONFISCO:</span> R$ {confisco_total:.2f}<br>
            • <span class="valor-amarelo">RENDIMENTO RESIDUAL (SOBRA FINAL):</span> R$ {sobra_residual:.2f}<br>
            • <span class="expro-destaque">DEPRECIAÇÃO DA FORÇA DE TRABALHO:</span> {depreciacao_p:.1f}%
        </div>
    """, unsafe_allow_html=True)
