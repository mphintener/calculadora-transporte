import streamlit as st
import pandas as pd
from geodata import GEO_SPO 

# 1. IDENTIDADE VISUAL E FORÇAMENTO DE INTERFACE
st.set_page_config(page_title="Beta II - Calculadora do Trecho", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    
    /* TITULOS E LABELS */
    label, .stSelectbox label, .stNumberInput label { 
        color: #FFCC00 !important; font-weight: 800 !important; 
        text-transform: uppercase !important; font-size: 0.85rem !important;
    }

    /* FORÇAR VISIBILIDADE DO ÍCONE DE AJUDA (?) */
    /* Aumentamos o tamanho e mudamos a cor para Amarelo para destacar no preto */
    .stTooltipIcon {
        color: #FFCC00 !important; 
        font-size: 1.4rem !important;
        background-color: #E63946 !important; /* Fundo vermelho para virar um 'botão' */
        border-radius: 50% !important;
        padding: 2px !important;
    }

    .chamada-alerta { 
        background-color: #E63946; color: white; text-align: center; 
        padding: 10px; font-weight: 900; border: 2px solid #FFCC00; 
        margin-bottom: 8px; text-transform: uppercase; font-size: 1.1rem;
    }
    
    .stNumberInput input { background-color: #111 !important; color: #FFFFFF !important; font-size: 1.1rem !important; border: 1px solid #444 !important; }

    .sintese-box { 
        background-color: #111; border: 1px solid #FFCC00; 
        padding: 18px; margin-top: 10px; color: #FFFFFF; 
        font-family: 'Courier New', monospace; font-size: 1rem;
    }

    .nota-tecnica {
        background-color: #000; border: 1px solid #444; padding: 15px;
        margin-top: 15px; color: #AAA; font-size: 0.85rem; font-style: italic;
    }
    
    .expro-destaque { color: #E63946; font-weight: 900; }
    .valor-amarelo { color: #FFCC00; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

lista_geo = sorted(list(GEO_SPO.keys()))

st.markdown('<div class="chamada-alerta">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)

with st.form("form_beta_ii_visual_help"):
    st.markdown('<h4 style="color:#FFCC00; font-size:0.9rem;">📍 GEOGRAFIA E FLUXO</h4>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: moradia = st.selectbox("MORADIA (ORIGEM):", lista_geo, index=0)
    with c2: trabalho = st.selectbox("TRABALHO (DESTINO):", lista_geo, index=1)
    
    st.markdown('<h4 style="color:#FFCC00; font-size:0.9rem;">💵 ECONOMIA PESSOAL</h4>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    with r1: sal_bruto = st.number_input("SALÁRIO BRUTO (R$):", min_value=0.0, step=100.0, value=3000.0)
    # AQUI ESTÁ O CAMPO COM O ÍCONE DESTACADO
    with r2: custo_vida = st.number_input("CUSTO DE VIDA FIXO (R$):", min_value=0.0, step=50.0, value=0.0, 
                                         help="ESTE CAMPO É OPCIONAL. Digite aqui gastos com Aluguel, Comida e Contas. Ele serve para mostrar sua SOBRA FINAL após a expropriação do sistema.")
    
    st.markdown('<h4 style="color:#FFCC00; font-size:0.9rem;">🚌 CUSTOS DIÁRIOS (ÔNIBUS/METRÔ/TREM/APP/CARRO)</h4>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1: p_bus = st.number_input("🚌 ÔNIBUS (R$):", value=4.40)
    with g2: p_trem = st.number_input("🚆 METRÔ/TREM (R$):", value=5.00)
    with g3: p_integra = st.number_input("🔄 INTEGRAÇÃO (R$):", value=0.0)
    
    g4, g5 = st.columns(2)
    with g4: p_app = st.number_input("📱 APP/TÁXI (R$):", value=0.0)
    with g5: p_car = st.number_input("🚗 CARRO/COMBUST. (R$):", value=0.0)
    
    st.write("")
    col_d, col_h = st.columns(2)
    with col_d: dias_m = st.number_input("DIAS DE TRECHO NO MÊS:", 1, 31, 22)
    with col_h: h_dia = st.slider("TOTAL DE HORAS NO TRECHO / DIA:", 0.5, 12.0, 3.0, step=0.5)
    
    submit = st.form_submit_button("PROCESSAR IMPACTO REAL")

if submit:
    # LÓGICA TÉCNICA (EXPROPRIAÇÃO)
    h_pagas = 176
    v_hora_nom = sal_bruto / h_pagas if sal_bruto > 0 else 0
    custo_transp_diario = p_bus + p_trem + p_integra + p_app + p_car
    custo_transp_mensal = custo_transp_diario * dias_m
    h_trecho_mensal = h_dia * dias_m
    
    # CONFISCO: TARIFA + VALOR DO TEMPO EXPROPRIADO
    valor_tempo_expro = h_trecho_mensal * v_hora_nom
    confisco_total = custo_transp_mensal + valor_tempo_expro
    
    v_hora_real = (sal_bruto - custo_transp_mensal) / (h_pagas + h_trecho_mensal) if sal_bruto > 0 else 0
    depreciacao_p = (1 - (v_hora_real / v_hora_nom)) * 100 if v_hora_nom > 0 else 0
    sobra_residual = sal_bruto - custo_transp_mensal - custo_vida

    # VETOR DE FLUXO
    st.markdown('<h4 style="color:#FFCC00; font-size:0.9rem;">🗺️ FLUXO DE DESLOCAMENTO</h4>', unsafe_allow_html=True)
    st.markdown(f"""
        <div style="background: #111; padding: 25px; border: 1px solid #E63946; text-align: center;">
            <div style="display: flex; justify-content: space-around; align-items: center;">
                <div style="color: #FFCC00; font-weight: bold;">🏠 {moradia}</div>
                <div style="color: #E63946; font-size: 1.5rem; margin: 0 15px;">⚡――――▶</div>
                <div style="color: #FFCC00; font-weight: bold;">💼 {trabalho}</div>
            </div>
            <p style="color:#E63946; font-size:0.85rem; margin-top:15px; font-weight:bold; border-top: 1px solid #333; padding-top:10px;">
                CASA-TRABALHO-CASA É TEMPO DE TRABALHO NÃO PAGO
            </p>
        </div>
    """, unsafe_allow_html=True)

    # MÉTRICAS CONSOLIDADAS
    st.markdown('<h4 style="color:#FFCC00; font-size:0.9rem;">🔬 MÉTRICAS CONSOLIDADAS</h4>', unsafe_allow_html=True)
    label_sobra = "SOBRA FINAL (APÓS CUSTO DE VIDA):" if custo_vida > 0 else "SALÁRIO LÍQUIDO DO TRANSPORTE:"
    
    st.markdown(f"""
        <div class="sintese-box">
            • <span class="valor-amarelo">VALOR DA HORA TRABALHADA:</span> De R$ {v_hora_nom:.2f} para <span class="expro-destaque">R$ {v_hora_real:.2f}</span><br>
            • <span class="expro-destaque">TEMPO DE VIDA NO TRECHO:</span> {h_trecho_mensal:.1f}h/mês<br>
            • <span class="valor-amarelo">VALOR DO CONFISCO (TARIFA + TEMPO DE TRABALHO NÃO PAGO):</span> R$ {confisco_total:,.2f}<br>
            • <span class="valor-amarelo">{label_sobra}</span> R$ {sobra_residual:,.2f}<br>
            • <span class="expro-destaque">DEPRECIAÇÃO DA FORÇA DE TRABALHO:</span> {depreciacao_p:.1f}%
        </div>
    """, unsafe_allow_html=True)

    # NOTA EXPLICATIVA
    st.markdown(f"""
        <div class="nota-tecnica">
            <b>NOTA TÉCNICA:</b> O valor do "Confisco" reflete o que o sistema retira de você. Ele soma o dinheiro gasto com tarifas 
            ao valor monetário do seu tempo (que consideramos trabalho não remunerado). 
            Se você morasse ao lado do trabalho, este valor estaria no seu bolso ou seria tempo de descanso.
        </div>
    """, unsafe_allow_html=True)
