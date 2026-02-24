import streamlit as st

# --- 1. CONFIGURAÇÃO DE APLICATIVO (PWA) ---
st.markdown("""
    <link rel="manifest" href="https://raw.githubusercontent.com/mphintener/calculadora-transporte/main/manifest.json">
    <meta name="theme-color" content="#FFCC00">
    <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/mphintener/calculadora-transporte/main/logo.png">
""", unsafe_allow_html=True)

# --- 2. CONFIGURAÇÃO DA PÁGINA E ESTILO ---
st.set_page_config(page_title="Calculadora do Trecho", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .stButton>button { background-color: #FFCC00; color: #000000; font-weight: bold; width: 100%; border: none; height: 3.5em; border-radius: 5px; }
    .stButton>button:hover { background-color: #E63946; color: #FFFFFF; }
    h1, h2, h3, h4, span, label, p { font-family: 'Courier New', monospace; }
    label { color: #FFCC00 !important; font-size: 1rem !important; font-weight: bold; }
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div { 
        background-color: #111 !important; color: white !important; border: 1px solid #333 !important; 
    }
    .report-box { background:#111; padding:20px; border:1px solid #FFCC00; border-radius:5px; line-height:1.6; }
</style>
""", unsafe_allow_html=True)

# --- 3. TÍTULO E CABEÇALHO ---
st.title("📊 CALCULADORA DO TRECHO")
st.subheader("Diagnóstico de Rendimento Real e Mobilidade Urbana")
st.write("---")

# --- 4. FORMULÁRIO CENTRALIZADO (Para Celular) ---
with st.form("diagnostico_principal"):
    st.markdown("### 👤 PERFIL E LOCALIDADE")
    c1, c2 = st.columns(2)
    with c1:
        idade = st.number_input("IDADE", min_value=14, value=30)
        escolaridade = st.selectbox("ESCOLARIDADE", ["Fundamental", "Médio", "Técnico", "Superior", "Pós-Graduação"])
        setor = st.text_input("SETOR DE ATIVIDADE", "Serviços")
    with c2:
        moradia = st.text_input("LOCAL DE MORADIA", "Caieiras")
        trabalho = st.text_input("LOCAL DE TRABALHO", "São Paulo")
    
    st.write("---")
    st.markdown("### 💰 CUSTOS E TEMPO")
    c3, c4 = st.columns(2)
    with c3:
        sal_bruto = st.number_input("SALÁRIO BRUTO (R$)", value=3000.0)
        custo_vida = st.number_input("CUSTO DE VIDA (ALUGUEL/COMIDA) (R$)", value=1500.0)
        h_dia = st.number_input("HORAS NO TRECHO (DIÁRIO)", value=2.0)
    with c4:
        dias_m = st.number_input("DIAS TRABALHADOS/MÊS", value=22)
        v_transp_dia = st.number_input("GASTO TOTAL TRANSPORTE/DIA (R$)", value=10.0)

    submit = st.form_submit_button("EFETUAR DIAGNÓSTICO ESTRATÉGICO")

# --- 5. LÓGICA E RESULTADOS ---
if submit:
    # Cálculos Técnicos
    custo_transp_m = v_transp_dia * dias_m
    v_hora_nom = sal_bruto / 176
    h_mensal = h_dia * dias_m
    rend_disponivel = sal_bruto - custo_transp_m
    sobra_final = rend_disponivel - custo_vida
    v_hora_real = rend_disponivel / (176 + h_mensal)
    confisco = custo_transp_m + (h_mensal * v_hora_nom)
    depre = (1 - (v_hora_real / v_hora_nom)) * 100

    st.error("🚨 ALERTA DE EXPROPRIAÇÃO MENSAL")

    # Vetor de Fluxo
    st.markdown(f"""
    <div style="background:#000; padding:25px; border:1px solid #E63946; text-align:center; margin-bottom:20px;">
        <div style="color:#FFCC00; font-weight:bold; font-size:1.4rem;">
            🏠 {moradia.upper()} <span style="color:#E63946;">—————▶</span> 💼 {trabalho.upper()}
        </div>
        <div style="margin-top:15px; border-top:1px solid #333; padding-top:10px; color:#E63946; font-weight:bold;">
            CASA-TRABALHO-CASA É TEMPO DE TRABALHO NÃO PAGO<br>
            <span style="color:#FFCC00;">PERFIL: {idade} ANOS | {escolaridade.upper()} | {setor.upper()}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Métricas
    st.markdown(f"""
    <div class="report-box">
        <h4 style="color:#FFCC00; margin-top:0;">🔬 MÉTRICAS CONSOLIDADAS</h4>
        <p>• <b style="color:#FFCC00;">VALOR DA HORA TRABALHADA:</b> De R$ {v_hora_nom:.2f} para <b style="color:#E63946;">R$ {v_hora_real:.2f}</b></p>
        <p>• <b style="color:#E63946;">TEMPO DE VIDA NO TRECHO:</b> {h_mensal:.1f}h/mês</p>
        <p>• <b style="color:#FFCC00;">CONFISCO OPERACIONAL:</b> R$ {confisco:.2f}</p>
        <p>• <b style="color:#FFCC00;">RENDIMENTO DISPONÍVEL (PÓS-TRANSPORTE):</b> R$ {rend_disponivel:.2f}</p>
        <p>• <b style="color:#FFCC00;">SOBRA RESIDUAL (PÓS-CUSTO DE VIDA):</b> R$ {sobra_final:.2f}</p>
        <p>• <b style="color:#E63946;">DEPRECIAÇÃO DA FORÇA DE TRABALHO:</b> {depre:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)

    # Nota Técnica
    st.markdown("""
    <div style="background-color: #000; padding: 20px; border: 1px solid #333; margin-top: 25px; color: #FFF; font-size: 0.9rem;">
        <b style="color: #FFCC00;">NOTA TÉCNICA:</b> O "CONFISCO" REFLETE O VALOR SUBTRAÍDO DO RENDIMENTO REAL. 
        O TRECHO É CONSIDERADO TRABALHO NÃO PAGO POIS É ESSENCIAL PARA A REPRODUÇÃO DA FORÇA DE TRABALHO.
    </div>
    """, unsafe_allow_html=True)

    # Download
    relatorio = f"DIAGNÓSTICO: {moradia} -> {trabalho}\nRENDIMENTO DISPONÍVEL: R$ {rend_disponivel:.2f}\nCONFISCO: R$ {confisco:.2f}"
    st.download_button("📥 GERAR RELATÓRIO TÉCNICO (.TXT)", relatorio, file_name=f"diagnostico_{moradia}.txt")
