import streamlit as st

# 1. CONFIGURAÇÃO E IDENTIDADE VISUAL
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
    .alerta-vermelho { background-color: #E63946; color: white; padding: 15px; text-align: center; font-weight: bold; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. CABEÇALHO
st.title("📊 CALCULADORA DO TRECHO")
st.subheader("Análise de Expropriação do Tempo e Rendimento Real")

# 3. ENTRADA DE DADOS ORGANIZADA (Sugestão de Expander)
with st.expander("📝 CLIQUE AQUI PARA CONFIGURAR SEU PERFIL E CUSTOS", expanded=True):
    with st.form("main_form"):
        c1, c2 = st.columns(2)
        with c1:
            idade = st.number_input("IDADE", value=30)
            escolaridade = st.selectbox("ESCOLARIDADE", ["Fundamental", "Médio", "Técnico", "Superior", "Pós-Graduação"])
            setor = st.text_input("SETOR DE ATIVIDADE", "Serviços")
            salario = st.number_input("SALÁRIO BRUTO (R$)", value=3000.0)
        with c2:
            moradia = st.text_input("LOCAL DE MORADIA", "Caieiras")
            trabalho = st.text_input("LOCAL DE TRABALHO", "São Paulo")
            h_dia = st.number_input("HORAS NO TRECHO (DIÁRIO)", value=2.0)
            v_dia = st.number_input("GASTO TRANSPORTE/DIA (R$)", value=10.0)
            custo_v = st.number_input("CUSTO DE VIDA (ALUGUEL/COMIDA) (R$)", value=1500.0)
        
        submit = st.form_submit_button("EFETUAR DIAGNÓSTICO ESTRATÉGICO")

# 4. LÓGICA TÉCNICA E RESULTADOS
if submit:
    # Cálculos
    dias_mes = 22
    c_transp_m = v_dia * dias_mes
    v_hora_nom = salario / 176
    h_mensal_trecho = h_dia * dias_mes
    rend_disponivel = salario - c_transp_m
    sobra_final = rend_disponivel - custo_v
    v_hora_real = rend_disponivel / (176 + h_mensal_trecho)
    confisco = c_transp_m + (h_mensal_trecho * v_hora_nom)
    depreciação = (1 - (v_hora_real / v_hora_nom)) * 100

    # Vetor de Fluxo Visual
    st.markdown(f"""
    <div style="background:#000; padding:20px; border:1px solid #E63946; text-align:center; margin: 20px 0;">
        <div style="color:#FFCC00; font-weight:bold; font-size:1.2rem;">
            🏠 {moradia.upper()} <span style="color:#E63946;">—————▶</span> 💼 {trabalho.upper()}
        </div>
        <div style="margin-top:10px; color:#FFCC00; font-size:0.9rem;">
            PERFIL: {idade} ANOS | {escolaridade.upper()} | {setor.upper()}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="alerta-vermelho">🚨 ALERTA DE EXPROPRIAÇÃO MENSAL IDENTIFICADO</div>', unsafe_allow_html=True)

    # Bloco de Métricas
    st.markdown(f"""
    <div class="report-box">
        <p>• <b>VALOR DA HORA REAL:</b> De R$ {v_hora_nom:.2f} para <span style="color:#E63946;">R$ {v_hora_real:.2f}</span></p>
        <p>• <b>CONFISCO OPERACIONAL:</b> R$ {confisco:.2f}</p>
        <p>• <b>RENDIMENTO DISPONÍVEL:</b> R$ {rend_disponivel:.2f}</p>
        <p>• <b>SOBRA RESIDUAL (PÓS-CUSTO DE VIDA):</b> R$ {sobra_final:.2f}</p>
        <p>• <b>DEPRECIAÇÃO DA FORÇA DE TRABALHO:</b> {depreciação:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)
# Bloco de Nota Técnica Direta
    st.markdown(f"""
    <div style="background-color: #000; padding: 20px; border: 1px solid #333; margin-top: 25px; color: #FFF; font-size: 0.95rem; border-left: 5px solid #FFCC00;">
        <b style="color: #FFCC00;">NOTA TÉCNICA:</b><br>
        O diagnóstico identifica que o trajeto entre <b>{moradia.upper()}</b> e <b>{trabalho.upper()}</b> 
        constitui um fluxo de <b>Expropriação do Tempo</b>. As {h_mensal_trecho} horas mensais em trânsito 
        representam uma jornada extraordinária compulsória e não remunerada, resultando em 
        <b>Confisco Operacional</b> do rendimento real.
    </div>
    """, unsafe_allow_html=True)

    # Botão de Exportação
    relatorio_txt = f"""NOTA TÉCNICA - CALCULADORA DO TRECHO
-------------------------------------------
PERFIL: {idade} anos | {escolaridade} | {setor}
FLUXO: {moradia} -> {trabalho}
RENDIMENTO DISPONÍVEL: R$ {rend_disponivel:.2f}
SOBRA RESIDUAL: R$ {sobra_final:.2f}
CONFISCO TOTAL: R$ {confisco:.2f}
DEPRECIAÇÃO: {depreciação:.1f}%
-------------------------------------------
O tempo de trecho é trabalho não pago."""

    st.download_button("📥 BAIXAR NOTA TÉCNICA (.TXT)", relatorio_txt, file_name=f"nota_tecnica_{moradia}.txt")
   
