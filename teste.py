import streamlit as st
from geodata import GEO_SPO 
# --- CÓDIGO DE ATIVAÇÃO DO APLICATIVO (PWA) ---
# Isso permite que o usuário "Instale" a calculadora no celular
st.markdown("""
    <link rel="manifest" href="https://raw.githubusercontent.com/SEU_USUARIO/calculadora-transporte/main/manifest.json">
    <meta name="theme-color" content="#FFCC00">
    <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/SEU_USUARIO/calculadora-transporte/main/logo.png">
""", unsafe_allow_html=True)
# ----------------------------------------------
# 1. IDENTIDADE VISUAL (CSS)
st.set_page_config(page_title="Calculadora do Trecho", layout="centered")
    
st.markdown('<style>'
    # Remove a faixa branca e o header padrão do Streamlit
    '[data-testid="stHeader"] { display: none !important; } '
    'div.block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; } '
    
    # Garante o fundo preto em tudo
    '[data-testid="stAppViewContainer"], .stApp, [data-testid="stSidebar"], [data-testid="stSidebarContent"] '
    '{ background-color: #000000 !important; } '
    'section[data-testid="stSidebar"] > div { background-color: #000000 !important; } '
    
    # Tipografia e Alertas
    'label { color: #FFCC00 !important; font-weight: bold; text-transform: uppercase; font-size: 0.85rem; } '
    '.alerta-topo { background-color: #E63946; color: white; text-align: center; padding: 15px; font-weight: 900; border: 2px solid #FFCC00; width: 100%; } '
    '.subtitulo { color: #FFCC00; text-align: center; font-weight: 900; margin-top: 15px; margin-bottom: 25px; text-transform: uppercase; font-size: 1.1rem; } '
    '.secao-titulo { color: #FFCC00; font-weight: bold; font-size: 0.9rem; margin-top: 15px; margin-bottom: 5px; } '
    '</style>', unsafe_allow_html=True)

# Ícones
casa, trampo, raio, pin, money, bus, metr, intg, app, car, perfil = chr(0x1F3E0), chr(0x1F4BC), chr(0x26A1), chr(0x1F4CD), chr(0x1F4B5), chr(0x1F68C), chr(0x1F687), chr(0x1F504), chr(0x1F4F1), chr(0x1F697), chr(0x1F4DC)

# 2. SIDEBAR - PERFIL DO USUÁRIO
with st.sidebar:
    st.markdown(f'<h2 style="color:#FFCC00;">{perfil} PERFIL DO USUARIO</h2>', unsafe_allow_html=True)
    idade = st.number_input("IDADE:", 14, 100, 25)
    escolaridade = st.selectbox("ESCOLARIDADE:", ["Ensino Fundamental", "Ensino Medio Incompleto", "Ensino Medio Completo", "Superior Incompleto", "Superior Completo", "Pos-graduacao"])
    setor_atividade = st.selectbox("SETOR DE ATIVIDADE:", ["TI", "Telemarketing", "Construcao Civil", "Comercio", "Industria", "Logistica", "Outros"])

# 3. CABEÇALHO
st.markdown('<div class="alerta-topo">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">QUANTO DE TEMPO E DE DINHEIRO SÃO CONSUMIDOS NO SEU DESLOCAMENTO DIÁRIO?</div>', unsafe_allow_html=True)

# 4. FORMULÁRIO (BLOCO QUE VOCÊ POSSUI)
lista_geo = sorted(list(GEO_SPO.keys()))

with st.form("consultoria_form"):
    st.markdown(f'<p class="secao-titulo">{pin} GEOGRAFIA DO FLUXO PENDULAR</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        moradia = st.selectbox("MORADIA (ORIGEM):", lista_geo)
    with c2:
        trabalho = st.selectbox("TRABALHO (DESTINO):", lista_geo)

    st.markdown(f'<p class="secao-titulo">{money} ECONOMIA PESSOAL</p>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        sal_bruto = st.number_input("SALÁRIO BRUTO (R$):", value=0.0)
    with c4:
        custo_vida = st.number_input("CUSTO DE VIDA FIXO (R$):", value=0.0, help="Aluguel, alimentação, etc.")

    st.markdown(f'<p class="secao-titulo">{bus} CUSTOS DIÁRIOS (IDA+VOLTA)</p>', unsafe_allow_html=True)
    f1, f2, f3 = st.columns(3)
    v_bus = f1.number_input(f"{bus} ÔNIBUS (R$):", value=0.0)
    v_trem = f2.number_input(f"{metr} METRÔ/TREM (R$):", value=0.0)
    v_int = f3.number_input(f"{intg} INTEGRAÇÃO (R$):", value=0.0)
    
    f4, f5 = st.columns(2)
    v_app = f4.number_input(f"{app} APP/TÁXI (R$):", value=0.0)
    v_carro = f5.number_input(f"{car} CARRO/COMBUST. (R$):", value=0.0)
    
    st.divider()
    h_dia = st.slider("TEMPO NO TRECHO (HORAS IDA+VOLTA/DIA):", 0.0, 10.0, 2.5)
    dias_m = st.number_input("DIAS TRABALHADOS POR MÊS:", 0, 31, 22)

    # ESTA DEVE SER A ÚNICA LINHA DE BOTÃO DENTRO DO FORMULÁRIO
    submit = st.form_submit_button("EFETUAR DIAGNÓSTICO")
if submit:
    # --- 1. LÓGICA TÉCNICA E CÁLCULOS ---
    custo_transporte_m = (v_bus + v_trem + v_int + v_app + v_carro) * dias_m
    v_hora_nom = sal_bruto / 176 if sal_bruto > 0 else 0
    h_mensal = h_dia * dias_m
    rend_disponivel = sal_bruto - custo_transporte_m
    sobra_final = rend_disponivel - custo_vida 
    v_hora_real = rend_disponivel / (176 + h_mensal) if sal_bruto > 0 else 0
    confisco = custo_transporte_m + (h_mensal * v_hora_nom)
    depre = (1 - (v_hora_real / v_hora_nom)) * 100 if v_hora_nom > 0 else 0

    # --- 2. VETOR DE FLUXO ---
    fluxo_html = (
        '<div style="background:#000;padding:25px;border:1px solid #E63946;text-align:center;margin-top:20px;">'
        f'<div style="color:#FFCC00;font-weight:bold;font-size:1.2rem;">'
        f'{casa} {moradia.upper()} <span style="color:#E63946;">{raio} —————▶</span> {trampo} {trabalho.upper()}</div>'
        '<div style="margin-top:15px;border-top:1px solid #333;padding-top:10px;color:#E63946;font-weight:bold;font-size:0.9rem;">'
        'CASA-TRABALHO-CASA É TEMPO DE TRABALHO NÃO PAGO<br>'
        f'<span style="color:#FFCC00;">PERFIL: {idade} ANOS | {escolaridade.upper()} | {setor_atividade.upper()}</span></div>'
        '</div>'
    )
    st.markdown(fluxo_html, unsafe_allow_html=True)

    # --- 3. MÉTRICAS CONSOLIDADAS ---
    metrics_html = (
        f'<div style="background:#111;padding:20px;margin-top:20px;color:#FFF;border:1px solid #FFCC00;line-height:1.8;">'
        f'<h4 style="color:#FFCC00;margin-top:0;">{chr(0x1F52C)} MÉTRICAS CONSOLIDADAS</h4>'
        f'• <span style="color:#FFCC00;font-weight:bold;">VALOR DA HORA TRABALHADA:</span> De R$ {v_hora_nom:.2f} para <span style="color:#E63946;">R$ {v_hora_real:.2f}</span><br>'
        f'• <span style="color:#E63946;font-weight:bold;">TEMPO DE VIDA NO TRECHO:</span> {h_mensal:.1f}h/mês<br>'
        f'• <span style="color:#FFCC00;font-weight:bold;">CONFISCO OPERACIONAL (TARIFA + TEMPO DE TRABALHO NÃO PAGO):</span> R$ {confisco:.2f}<br>'
        f'• <span style="color:#FFCC00;font-weight:bold;">RENDIMENTO DISPONÍVEL (PÓS-TRANSPORTE):</span> R$ {rend_disponivel:.2f}<br>'
        f'• <span style="color:#FFCC00;font-weight:bold;">SOBRA RESIDUAL (PÓS-CUSTO DE VIDA):</span> R$ {sobra_final:.2f}<br>'
        f'• <span style="color:#E63946;font-weight:bold;">DEPRECIAÇÃO DA FORÇA DE TRABALHO:</span> {depre:.1f}%'
        '</div>'
    )
    st.markdown(metrics_html, unsafe_allow_html=True)

    # --- 4. NOTA TÉCNICA ---
    nota_html = (
        '<div style="background-color: #000; padding: 20px; border: 1px solid #333; margin-top: 25px; color: #FFF; font-size: 0.9rem; line-height: 1.6;">'
        '<b style="color: #FFCC00; font-size: 1rem; text-transform: uppercase;">NOTA TÉCNICA:</b><br><br>'
        'O <span style="color:#FFCC00; font-weight:bold;">"CONFISCO"</span> REFLETE O VALOR TOTAL SUBTRAÍDO DO RENDIMENTO REAL DO TRABALHADOR. '
        'ELE SOMA O GASTO DIRETO EM TARIFAS AO VALOR MONETÁRIO DO TEMPO DE DESLOCAMENTO (CALCULADO SOBRE O VALOR DA HORA NOMINAL). '
        'CONSIDERAMOS O TRECHO COMO <span style="color:#E63946; font-weight:bold;">"TRABALHO NÃO PAGO"</span> POIS É UM TEMPO OBRIGATÓRIO PARA A '
        'REPRODUÇÃO DA FORÇA DE TRABALHO, MAS NÃO REMUNERADO.'
        '</div>'
    )
    st.markdown(nota_html, unsafe_allow_html=True)

    # --- 5. DOWNLOAD DIRETO ---
    relatorio_texto = (
        "DIAGNÓSTICO DE MOBILIDADE E RENDIMENTO REAL\n"
        "-------------------------------------------\n"
        f"PERFIL: {idade} ANOS | {escolaridade.upper()} | {setor_atividade.upper()}\n"
        f"FLUXO: {moradia.upper()} >>> {trabalho.upper()}\n\n"
        "INDICADORES FINANCEIROS:\n"
        f"- VALOR HORA NOMINAL: R$ {v_hora_nom:.2f}\n"
        f"- VALOR HORA REAL: R$ {v_hora_real:.2f}\n"
        f"- CONFISCO OPERACIONAL (TARIFA + TEMPO DE TRABALHO NÃO PAGO): R$ {confisco:.2f}\n"
        f"- RENDIMENTO DISPONÍVEL (PÓS-TRANSPORTE): R$ {rend_disponivel:.2f}\n"
        f"- SOBRA RESIDUAL (PÓS-CUSTO DE VIDA): R$ {sobra_final:.2f}\n"
        f"- ÍNDICE DE DEPRECIAÇÃO: {depre:.1f}%\n\n"
        "NOTA TÉCNICA:\n"
        "O 'CONFISCO' REFLETE O VALOR TOTAL SUBTRAÍDO DO RENDIMENTO REAL DO TRABALHADOR. "
        "O TRECHO CASA-TRABALHO-CASA É CONSIDERADO TRABALHO NÃO PAGO."
    )

    st.markdown('<br>', unsafe_allow_html=True)
    st.download_button(
        label=f"{chr(0x1F4E5)} GERAR RELATÓRIO TÉCNICO (.TXT)",
        data=relatorio_texto,
        file_name=f"diagnostico_{moradia}_{trabalho}.txt",
        mime="text/plain",
    )
