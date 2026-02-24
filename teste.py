import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA E IDENTIDADE VISUAL
st.set_page_config(page_title="Calculadora do Trecho", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; color: #FFFFFF; }
    .stButton>button { background-color: #FFCC00; color: black; font-weight: bold; width: 100%; border-radius: 5px; border: none; }
    .stButton>button:hover { background-color: #E63946; color: white; }
    .alerta-topo { background-color: #E63946; color: white; padding: 15px; text-align: center; font-weight: bold; font-size: 1.5rem; margin-bottom: 20px; }
    label { color: #FFCC00 !important; font-weight: bold; }
    .stTextInput>div>div>input, .stNumberInput>div>div>input { background-color: #111; color: white; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 CALCULADORA DO TRECHO")
st.subheader("Diagnóstico Estratégico de Rendimento Real e Mobilidade")

# 2. FORMULÁRIO DE ENTRADA
with st.form("consultoria_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        idade = st.number_input("IDADE", min_value=14, max_value=100, value=30)
        escolaridade = st.selectbox("ESCOLARIDADE", ["Fundamental", "Médio", "Técnico", "Superior", "Pós-Graduação"])
        setor_atividade = st.text_input("SETOR DE ATIVIDADE", "Serviços")
        sal_bruto = st.number_input("SALÁRIO BRUTO (R$)", min_value=0.0, value=3000.0)
        custo_vida = st.number_input("CUSTO DE VIDA MENSAL (ALUGUEL, COMIDA, ETC) (R$)", min_value=0.0, value=1500.0)

    with col2:
        moradia = st.text_input("LOCAL DE MORADIA (Bairro/Cidade)", "Caieiras")
        trabalho = st.text_input("LOCAL DE TRABALHO (Bairro/Cidade)", "São Paulo")
        h_dia = st.number_input("HORAS NO TRECHO (DIÁRIO - IDA E VOLTA)", min_value=0.0, max_value=24.0, value=2.0)
        dias_m = st.number_input("DIAS TRABALHADOS NO MÊS", min_value=1, max_value=31, value=22)
        
        st.write("**GASTOS DIÁRIOS COM TRANSPORTE (R$)**")
        v_bus = st.number_input("ÔNIBUS", min_value=0.0, value=0.0)
        v_trem = st.number_input("TREM/METRÔ", min_value=0.0, value=0.0)
        v_carro = st.number_input("CARRO (Combustível/Estac.)", min_value=0.0, value=0.0)
        v_app = st.number_input("APP/TAXI", min_value=0.0, value=0.0)
        v_int = st.number_input("INTERMUNICIPAL", min_value=0.0, value=0.0)

    submit = st.form_submit_button("EFETUAR DIAGNÓSTICO ESTRATÉGICO")

# 3. LÓGICA TÉCNICA E RESULTADOS
if submit:
    # Cálculos
    custo_transporte_m = (v_bus + v_trem + v_int + v_app + v_carro) * dias_m
    v_hora_nom = sal_bruto / 176 if sal_bruto > 0 else 0
    h_mensal = h_dia * dias_m
    rend_disponivel = sal_bruto - custo_transporte_m
    sobra_final = rend_disponivel - custo_vida 
    v_hora_real = rend_disponivel / (176 + h_mensal) if sal_bruto > 0 else 0
    confisco = custo_transporte_m + (h_mensal * v_hora_nom)
    depre = (1 - (v_hora_real / v_hora_nom)) * 100 if v_hora_nom > 0 else 0

    st.markdown('<div class="alerta-topo">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)

    # Vetor de Fluxo
    fluxo_html = f"""
    <div style="background:#000;padding:25px;border:1px solid #E63946;text-align:center;margin-top:20px;">
        <div style="color:#FFCC00;font-weight:bold;font-size:1.2rem;">
            🏠 {moradia.upper()} <span style="color:#E63946;">—————▶</span> 💼 {trabalho.upper()}
        </div>
        <div style="margin-top:15px;border-top:1px solid #333;padding-top:10px;color:#E63946;font-weight:bold;font-size:0.9rem;">
            CASA-TRABALHO-CASA É TEMPO DE TRABALHO NÃO PAGO<br>
            <span style="color:#FFCC00;">PERFIL: {idade} ANOS | {escolaridade.upper()} | {setor_atividade.upper()}</span>
        </div>
    </div>
    """
    st.markdown(fluxo_html, unsafe_allow_html=True)

    # Métricas Consolidadas
    metrics_html = f"""
    <div style="background:#111;padding:20px;margin-top:20px;color:#FFF;border:1px solid #FFCC00;line-height:1.8;">
        <h4 style="color:#FFCC00;margin-top:0;">🔬 MÉTRICAS CONSOLIDADAS</h4>
        • <span style="color:#FFCC00;font-weight:bold;">VALOR DA HORA TRABALHADA:</span> De R$ {v_hora_nom:.2f} para <span style="color:#E63946;">R$ {v_hora_real:.2f}</span><br>
        • <span style="color:#E63946;font-weight:bold;">TEMPO DE VIDA NO TRECHO:</span> {h_mensal:.1f}h/mês<br>
        • <span style="color:#FFCC00;font-weight:bold;">CONFISCO OPERACIONAL (TARIFA + TEMPO DE TRABALHO NÃO PAGO):</span> R$ {confisco:.2f}<br>
        • <span style="color:#FFCC00;font-weight:bold;">RENDIMENTO DISPONÍVEL (PÓS-TRANSPORTE):</span> R$ {rend_disponivel:.2f}<br>
        • <span style="color:#FFCC00;font-weight:bold;">SOBRA RESIDUAL (PÓS-CUSTO DE VIDA):</span> R$ {sobra_final:.2f}<br>
        • <span style="color:#E63946;font-weight:bold;">DEPRECIAÇÃO DA FORÇA DE TRABALHO:</span> {depre:.1f}%
    </div>
    """
    st.markdown(metrics_html, unsafe_allow_html=True)

    # Nota Técnica
    st.markdown(f"""
    <div style="background-color: #000; padding: 20px; border: 1px solid #333; margin-top: 25px; color: #FFF; font-size: 0.9rem; line-height: 1.6;">
        <b style="color: #FFCC00; font-size: 1rem; text-transform: uppercase;">NOTA TÉCNICA:</b><br><br>
        O <b>"CONFISCO"</b> REFLETE O VALOR TOTAL SUBTRAÍDO DO RENDIMENTO REAL DO TRABALHADOR. 
        ELE SOMA O GASTO DIRETO EM TARIFAS AO VALOR MONETÁRIO DO TEMPO DE DESLOCAMENTO. 
        CONSIDERAMOS O TRECHO COMO <b>"TRABALHO NÃO PAGO"</b> POIS É UM TEMPO OBRIGATÓRIO PARA A REPRODUÇÃO DA FORÇA DE TRABALHO.
    </div>
    """, unsafe_allow_html=True)

    # Relatório para Download
    relatorio_texto = f"""DIAGNÓSTICO DE MOBILIDADE E RENDIMENTO REAL
-------------------------------------------
PERFIL: {idade} ANOS | {escolaridade.upper()} | {setor_atividade.upper()}
FLUXO: {moradia.upper()} >>> {trabalho.upper()}

INDICADORES FINANCEIROS:
- VALOR HORA NOMINAL: R$ {v_hora_nom:.2f}
- VALOR HORA REAL: R$ {v_hora_real:.2f}
- CONFISCO OPERACIONAL: R$ {confisco:.2f}
- RENDIMENTO DISPONÍVEL (PÓS-TRANSPORTE): R$ {rend_disponivel:.2f}
- SOBRA RESIDUAL (PÓS-CUSTO DE VIDA): R$ {sobra_final:.2f}
- ÍNDICE DE DEPRECIAÇÃO: {depre:.1f}%
"""
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button("📥 GERAR RELATÓRIO TÉCNICO (.TXT)", relatorio_texto, file_name=f"diagnostico_{moradia}.txt")
