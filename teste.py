import streamlit as st

# 1. CONFIGURAÇÃO E IDENTIDADE VISUAL (PRETO, AMARELO E VERMELHO)
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
    input { background-color: #111 !important; color: white !important; border: 1px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. TÍTULO E CABEÇALHO
st.title("📊 CALCULADORA DO TRECHO")
st.subheader("Diagnóstico Técnico de Expropriação do Tempo e Rendimento Real")

# 3. FORMULÁRIO COMPLETO (PERFIL, MODAIS E CUSTOS)
with st.form("diagnostico_mestre"):
    st.markdown("### 👤 PERFIL DO USUÁRIO")
    c1, c2, c3 = st.columns(3)
    with c1: 
        idade = st.number_input("👤 IDADE", min_value=14, value=30)
    with c2: 
        escolaridade = st.selectbox("🎓 ESCOLARIDADE", [
            "Fundamental Incompleto", "Fundamental Completo", 
            "Médio Incompleto", "Médio Completo", 
            "Técnico", "Superior Incompleto", "Superior Completo", 
            "Pós-Graduação", "Mestrado", "Doutorado"
        ])
    with c3: 
        setor = st.text_input("💼 SETOR DE ATIVIDADE", "Ex: Serviços, Indústria, TI")

    st.markdown("---")
    st.markdown("### 📍 LOCALIDADE E TEMPO")
    c4, c5, c6 = st.columns(3)
    with c4: 
        moradia = st.text_input("🏠 MORADIA (Cidade/Bairro)", "Caieiras")
    with c5: 
        trabalho = st.text_input("🏢 TRABALHO (Cidade/Bairro)", "São Paulo")
    with c6: 
        h_dia = st.number_input("⏳ HORAS NO TRECHO/DIA (Total)", value=2.0)

    st.markdown("---")
    st.markdown("### 🚌 CUSTOS DIÁRIOS DE TRANSPORTE (MODAIS)")
    t1, t2, t3, t4, t5 = st.columns(5)
    with t1: g_onibus = st.number_input("🚍 ÔNIBUS", min_value=0.0)
    with t2: g_metro = st.number_input("🚇 METRÔ", min_value=0.0)
    with t3: g_trem = st.number_input("🚆 TREM", min_value=0.0)
    with t4: g_app = st.number_input("🚗 APP", min_value=0.0)
    with t5: g_carro = st.number_input("⛽ CARRO/MOTO", min_value=0.0)

    st.markdown("---")
    st.markdown("### 💰 RENDIMENTOS E CUSTO DE VIDA")
    r1, r2, r3 = st.columns(3)
    with r1: 
        sal_bruto = st.number_input("💰 SALÁRIO BRUTO (R$)", min_value=0.0)
    with r2: 
        custo_vida = st.number_input("🏠 CUSTO DE VIDA (ALUGUEL/COMIDA) (R$)", min_value=0.0)
    with r3: 
        dias_m = st.number_input("📅 DIAS TRABALHADOS/MÊS", value=22)

    submit = st.form_submit_button("🚀 EFETUAR DIAGNÓSTICO ESTRATÉGICO")

# 4. LÓGICA DE CÁLCULO E RESULTADOS
if submit:
    gasto_diario = g_onibus + g_metro + g_trem + g_app + g_carro
    custo_transp_m = gasto_diario * dias_m
    v_hora_nom = sal_bruto / 176 if sal_bruto > 0 else 0
    h_mensal = h_dia * dias_m
    rend_disponivel = sal_bruto - custo_transp_m
    sobra_final = rend_disponivel - custo_vida
    v_hora_real = rend_disponivel / (176 + h_mensal) if (176 + h_mensal) > 0 else 0
    confisco = custo_transp_m + (h_mensal * v_hora_nom)
    depreciacao = (1 - (v_hora_real / v_hora_nom)) * 100 if v_hora_nom > 0 else 0

    # Vetor de Fluxo Visual
    st.markdown(f"""
    <div style="background:#000; padding:20px; border:1px solid #E63946; text-align:center; margin: 20px 0;">
        <div style="color:#FFCC00; font-weight:bold; font-size:1.4rem;">
            🏠 {moradia.upper()} <span style="color:#E63946;">—————▶</span> 💼 {trabalho.upper()}
        </div>
        <div style="margin-top:10px; color:#FFCC00; font-weight:bold;">
            ⚠️ EXPROPRIAÇÃO DETECTADA: {h_mensal:.1f}h/mês de Trabalho Não Pago<br>
            <span style="font-size:0.9rem;">PERFIL: {idade} ANOS | {escolaridade.upper()} | {setor.upper()}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<div style="background-color: #E63946; color: white; padding: 15px; text-align: center; font-weight: bold; border-radius: 5px;">
        🚨 ALERTA DE EXPROPRIAÇÃO MENSAL IDENTIFICADO
    </div>""", unsafe_allow_html=True)

    # Métricas Consolidadas
    st.markdown(f"""
    <div class="report-box">
        <h4 style="margin-top:0;">📋 RESULTADOS DO DIAGNÓSTICO</h4>
        <p>• 💹 <b>VALOR DA HORA REAL:</b> R$ {v_hora_real:.2f}</p>
        <p>• 💸 <b>CONFISCO OPERACIONAL:</b> R$ {confisco:.2f}</p>
        <p>• 💵 <b>RENDIMENTO DISPONÍVEL (PÓS-TRANSPORTE):</b> R$ {rend_disponivel:.2f}</p>
        <p>• 📉 <b>SOBRA RESIDUAL (PÓS-CUSTO DE VIDA):</b> R$ {sobra_final:.2f}</p>
        <p>• 📉 <b>DEPRECIAÇÃO DA FORÇA DE TRABALHO:</b> {depreciacao:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)

    # Nota Técnica
    st.markdown(f"""
    <div style="background-color: #111; padding: 20px; border-left: 5px solid #FFCC00; margin-top: 25px;">
        <b style="color: #FFCC00;">NOTA TÉCNICA:</b><br>
        O tempo de deslocamento entre {moradia} e {trabalho} via modais selecionados corrói o salário real, 
        resultando em <b>Confisco Operacional</b> e na expropriação da força de trabalho.
    </div>
    """, unsafe_allow_html=True)
