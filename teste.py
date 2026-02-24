import streamlit as st

# 1. IDENTIDADE VISUAL E CONFIGURAÇÃO
st.set_page_config(page_title="Calculadora do Trecho", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    h1, h2, h3, h4, label, p { color: #FFCC00 !important; font-family: 'Courier New', monospace; }
    .stButton>button { 
        background-color: #FFCC00 !important; color: #000000 !important; 
        font-weight: bold !important; width: 100%; border-radius: 5px; height: 3.5em; border: none;
    }
    .stButton>button:hover { background-color: #E63946 !important; color: #FFFFFF !important; }
    .report-box { background:#111; padding:20px; border:1px solid #FFCC00; border-radius:5px; margin-top:20px; }
    input { background-color: #111 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 CALCULADORA DO TRECHO")
st.subheader("Diagnóstico Técnico de Expropriação e Rendimento Real")

with st.form("diagnostico_detalhado"):
    # BLOCO 1: PERFIL
    st.markdown("### 👤 PERFIL E LOCALIDADE")
    c1, c2, c3, c4 = st.columns(4)
    with c1: idade = st.number_input("IDADE", min_value=14, step=1)
    with c2: escolaridade = st.selectbox("ESCOLARIDADE", ["Fundamental", "Médio", "Técnico", "Superior", "Pós-Graduação"])
    with c3: moradia = st.text_input("MORADIA (Bairro/Cidade)", "Caieiras")
    with c4: trabalho = st.text_input("TRABALHO (Bairro/Cidade)", "São Paulo")

    st.markdown("---")
    
    # BLOCO 2: CUSTOS DE TRANSPORTE DETALHADOS (O coração da análise)
    st.markdown("### 🚌 DETALHAMENTO DO TRECHO (GASTO DIÁRIO)")
    t1, t2, t3, t4, t5 = st.columns(5)
    with t1: g_onibus = st.number_input("🚍 ÔNIBUS (R$)", min_value=0.0, step=0.5)
    with t2: g_metro = st.number_input("🚇 METRÔ (R$)", min_value=0.0, step=0.5)
    with t3: g_trem = st.number_input("🚆 TREM (R$)", min_value=0.0, step=0.5)
    with t4: g_app = st.number_input("🚗 APP/UBER (R$)", min_value=0.0, step=1.0)
    with t5: g_carro = st.number_input("⛽ COMBUSTÍVEL (R$)", min_value=0.0, step=1.0)

    st.markdown("---")
    
    # BLOCO 3: RENDIMENTOS E TEMPO
    st.markdown("### 💰 RENDIMENTOS E TEMPO")
    r1, r2, r3, r4 = st.columns(4)
    with r1: sal_bruto = st.number_input("SALÁRIO BRUTO (R$)", min_value=0.0, step=100.0)
    with r2: custo_vida = st.number_input("CUSTO DE VIDA (R$)", min_value=0.0, step=100.0)
    with r3: h_trecho = st.number_input("HORAS NO TRECHO/DIA", min_value=0.0, step=0.5)
    with r4: dias_trab = st.number_input("DIAS TRABALHADOS/MÊS", value=22, step=1)

    submit = st.form_submit_button("🚀 EFETUAR DIAGNÓSTICO ESTRATÉGICO")

if submit:
    # Lógica de Cálculo
    gasto_diario_total = g_onibus + g_metro + g_trem + g_app + g_carro
    custo_transp_mes = gasto_diario_total * dias_trab
    v_hora_nom = sal_bruto / 176
    h_mensal_trecho = h_trecho * dias_trab
    rend_disponivel = sal_bruto - custo_transp_mes
    sobra_final = rend_disponivel - custo_vida
    v_hora_real = rend_disponivel / (176 + h_mensal_trecho)
    confisco = custo_transp_mes + (h_mensal_trecho * v_hora_nom)
    depreciacao = (1 - (v_hora_real / v_hora_nom)) * 100 if v_hora_nom > 0 else 0

    # Vetor de Fluxo Visual
    st.markdown(f"""
    <div style="background:#000; padding:20px; border:1px solid #E63946; text-align:center; margin: 20px 0;">
        <div style="color:#FFCC00; font-weight:bold; font-size:1.4rem;">
            🏠 {moradia.upper()} <span style="color:#E63946;">—————▶</span> 💼 {trab_upper := trabalho.upper()}
        </div>
        <div style="margin-top:10px; color:#FFCC00; font-weight:bold;">
            ⚠️ EXPROPRIAÇÃO DETECTADA: {h_mensal_trecho:.1f}h/mês de Trabalho Não Pago
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Métricas Consolidadas
    st.markdown(f"""
    <div class="report-box">
        <h4 style="margin-top:0;">📋 RESULTADOS DO DIAGNÓSTICO</h4>
        <p>• 💹 <b>VALOR DA HORA REAL:</b> R$ {v_hora_real:.2f}</p>
        <p>• 💸 <b>CONFISCO OPERACIONAL:</b> R$ {confisco:.2f}</p>
        <p>• 💵 <b>RENDIMENTO DISPONÍVEL:</b> R$ {rend_disponivel:.2f}</p>
        <p>• 📉 <b>SOBRA RESIDUAL (APÓS CUSTO DE VIDA):</b> R$ {sobra_final:.2f}</p>
        <p>• 📉 <b>DEPRECIAÇÃO DA FORÇA DE TRABALHO:</b> {depreciacao:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)

    # Nota Técnica
    st.markdown(f"""
    <div style="background-color: #111; padding: 20px; border-left: 5px solid #FFCC00; margin-top: 25px;">
        <b style="color: #FFCC00;">NOTA TÉCNICA:</b><br>
        O deslocamento entre {moradia} e {trabalho} via modais selecionados corrói o salário real, 
        resultando em um confisco de R$ {confisco:.2f} mensais entre tarifa e tempo expropriado.
    </div>
    """, unsafe_allow_html=True)
