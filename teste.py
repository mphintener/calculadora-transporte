import streamlit as st

# 1. IDENTIDADE VISUAL E CONFIGURAÇÃO
st.set_page_config(page_title="Calculadora do Trecho", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    h1, h2, h3, h4, label, p { color: #FFCC00 !important; font-family: 'Arial', sans-serif; }
    .stButton>button { 
        background-color: #FFCC00 !important; color: #000000 !important; 
        font-weight: bold !important; width: 100%; border-radius: 5px; height: 3.5em; border: none; font-size: 1.2rem;
    }
    .stButton>button:hover { background-color: #E63946 !important; color: #FFFFFF !important; }
    .report-box { background:#111; padding:25px; border:2px solid #FFCC00; border-radius:10px; margin-top:20px; font-size: 1.1rem; }
    input, select { background-color: #111 !important; color: white !important; border: 1px solid #444 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. TÍTULO E CHAMADA DIRETA
st.title("📊 CALCULADORA DO TRECHO")
st.subheader("Quanto de tempo e de dinheiro são consumidos no seu deslocamento diário?")

# 3. FORMULÁRIO COMPLETO
with st.form("diagnostico_mestre"):
    st.markdown("### 👤 PERFIL")
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
        setor = st.selectbox("💼 SETOR DE ATIVIDADE", [
            "Serviços", "Comércio", "Indústria", "Educação", "Saúde", "TI/Tecnologia", "Construção Civil", "Transportes", "Administração Pública", "Outros"
        ])

    st.markdown("---")
    st.markdown("### 🏠 LOCAL DE MORADIA")
    m1, m2 = st.columns(2)
    with m1: 
        municipio_moradia = st.text_input("MUNICÍPIO (Moradia)", "Ex: Caieiras")
    with m2: 
        distrito_moradia = st.text_input("DISTRITO/BAIRRO (Moradia)", "Ex: Laranjeiras")

    st.markdown("---")
    st.markdown("### 🏢 LOCAL DE TRABALHO")
    t1, t2, t3 = st.columns(3)
    with t1: 
        municipio_trabalho = st.text_input("MUNICÍPIO (Trabalho)", "Ex: São Paulo")
    with t2: 
        distrito_trabalho = st.text_input("DISTRITO/BAIRRO (Trabalho)", "Ex: Centro")
    with t3:
        h_dia = st.number_input("⏳ HORAS NO TRECHO (Total Ida/Volta)", value=2.0, step=0.5)

    st.markdown("---")
    st.markdown("### 🚌 CUSTOS DIÁRIOS DE TRANSPORTE (Ida/Volta)")
    tr1, tr2, tr3, tr4, tr5 = st.columns(5)
    with tr1: g_onibus = st.number_input("🚍 ÔNIBUS (R$)", min_value=0.0)
    with tr2: g_metro = st.number_input("🚇 METRÔ (R$)", min_value=0.0)
    with tr3: g_trem = st.number_input("🚆 TREM (R$)", min_value=0.0)
    with tr4: g_app = st.number_input("🚗 APP (R$)", min_value=0.0)
    with tr5: g_carro = st.number_input("⛽ COMBUSTÍVEL (R$)", min_value=0.0)

    st.markdown("---")
    st.markdown("### 💰 RENDIMENTOS E CUSTO DE VIDA")
    r1, r2, r3 = st.columns(3)
    with r1: 
        sal_bruto = st.number_input("💰 SALÁRIO BRUTO (R$)", min_value=0.0)
    with r2: 
        custo_vida = st.number_input("🏠 CUSTO DE VIDA (ALUGUEL/COMIDA) (R$) ? (Opcional)", min_value=0.0, value=0.0)
    with r3: 
        dias_m = st.number_input("📅 DIAS TRABALHADOS/MÊS", value=22)

    submit = st.form_submit_button("EFETUAR DIAGNÓSTICO")

# 4. LÓGICA E RESULTADOS
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
    <div style="background:#000; padding:25px; border:2px solid #E63946; text-align:center; margin: 20px 0;">
        <div style="color:#FFCC00; font-weight:bold; font-size:1.6rem;">
            🏠 {municipio_moradia.upper()} ({distrito_moradia.upper()}) <br>
            <span style="color:#E63946;">—————▶</span> <br>
            💼 {municipio_trabalho.upper()} ({distrito_trabalho.upper()})
        </div>
        <div style="margin-top:15px; color:#FFCC00; font-size:1.1rem;">
            <b>TEMPO EXPROPRIADO:</b> {h_mensal:.1f}h por mês<br>
            <small>PERFIL: {idade} ANOS | {escolaridade.upper()} | {setor.upper()}</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<div style="background-color: #E63946; color: white; padding: 15px; text-align: center; font-weight: bold; border-radius: 5px; font-size: 1.2rem;">
        🚨 ALERTA DE EXPROPRIAÇÃO MENSAL
    </div>""", unsafe_allow_html=True)

    # Resultados Consolidados
    st.markdown(f"""
    <div class="report-box">
        <h3 style="margin-top:0; color:#FFCC00;">📋 RESULTADOS</h3>
        <p>• 💹 <b>VALOR DA HORA REAL:</b> <span style="color:white;">R$ {v_hora_real:.2f}</span></p>
        <p>• 💸 <b>CONFISCO OPERACIONAL:</b> <span style="color:white;">R$ {confisco:.2f}</span></p>
        <p>• 💵 <b>RENDIMENTO DISPONÍVEL:</b> <span style="color:white;">R$ {rend_disponivel:.2f}</span></p>
        <p>• 📉 <b>SOBRA RESIDUAL (PÓS-CUSTO DE VIDA):</b> <span style="color:white;">R$ {sobra_final:.2f}</span></p>
        <p>• 📉 <b>DEPRECIAÇÃO DA FORÇA DE TRABALHO:</b> <span style="color:#E63946;">{depreciacao:.1f}%</span></p>
    </div>
    """, unsafe_allow_html=True)

    # Nota Técnica
    st.markdown(f"""
    <div style="background-color: #111; padding: 20px; border-left: 5px solid #FFCC00; margin-top: 25px; font-size: 1rem;">
        <b style="color: #FFCC00;">NOTA TÉCNICA:</b><br>
        O deslocamento entre {municipio_moradia} e {municipio_trabalho} é tempo de trabalho não pago que corrói seu salário real.
    </div>
    """, unsafe_allow_html=True)
