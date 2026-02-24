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
    input, select, .stSelectbox { background-color: #111 !important; color: white !important; border: 1px solid #444 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. BANCO DE DADOS GEOGRÁFICO (RMSP e Distritos SP)
municipios_rmsp = sorted(["Arujá", "Barueri", "Biritiba-Mirim", "Caieiras", "Cajamar", "Carapicuíba", "Cotia", "Diadema", "Embu das Artes", "Embu-Guaçu", "Ferraz de Vasconcelos", "Francisco Morato", "Franco da Rocha", "Guararema", "Guarulhos", "Itapecerica da Serra", "Itapevi", "Itaquaquecetuba", "Jandira", "Juquitiba", "Mairiporã", "Mauá", "Mogi das Cruzes", "Osasco", "Pirapora do Bom Jesus", "Poá", "Ribeirão Pires", "Rio Grande da Serra", "Salesópolis", "Santa Isabel", "Santana de Parnaíba", "Santo André", "São Bernardo do Campo", "São Caetano do Sul", "São Lourenço da Serra", "São Paulo", "Suzano", "Taboão da Serra", "Vargem Grande Paulista"])
distritos_sp = sorted(["Água Rasa", "Alto de Pinheiros", "Anhanguera", "Aricanduva", "Artur Alvim", "Barra Funda", "Bela Vista", "Belém", "Bom Retiro", "Brasilândia", "Butantã", "Cachoeirinha", "Cambuci", "Campo Belo", "Campo Grande", "Campo Limpo", "Cangaíba", "Capão Redondo", "Carrão", "Casa Verde", "Cidade Ademar", "Cidade Dutra", "Cidade Líder", "Cidade Tiradentes", "Consolação", "Cursino", "Ermelino Matarazzo", "Freguesia do Ó", "Grajaú", "Guaianases", "Iguatemi", "Ipiranga", "Itaim Bibi", "Itaim Paulista", "Itaquera", "Jabaquara", "Jaçanã", "Jaguara", "Jaguaré", "Jaraguá", "Jardim Ângela", "Jardim Helena", "Jardim Paulista", "Jardim São Luís", "Lapa", "Liberdade", "Limão", "Mandaqui", "Marsilac", "Moema", "Mooca", "Morumbi", "Parelheiros", "Pari", "Parque do Carmo", "Pedreira", "Penha", "Perdizes", "Perus", "Pinheiros", "Pirituba", "Ponte Rasa", "Raposo Tavares", "República", "Rio Pequeno", "Sacomã", "Santa Cecília", "Santana", "Santo Amaro", "São Domingos", "São Lucas", "São Mateus", "São Miguel", "São Rafael", "Sapopemba", "Saúde", "Sé", "Socorro", "Tatuapé", "Tremembé", "Tucuruvi", "Vila Andrade", "Vila Curuçá", "Vila Formosa", "Vila Guilherme", "Vila Jacuí", "Vila Leopoldina", "Vila Maria", "Vila Mariana", "Vila Matilde", "Vila Medeiros", "Vila Prudente", "Vila Sônia"])

st.title("📊 CALCULADORA DO TRECHO")
st.subheader("Quanto de tempo e de dinheiro são consumidos no seu deslocamento diário?")

# 3. FORMULÁRIO COMPLETO
with st.form("diagnostico_mestre"):
    st.markdown("### 👤 PERFIL")
    c1, c2, c3 = st.columns(3)
    with c1: idade = st.number_input("👤 IDADE", min_value=14, value=30)
    with c2: escolaridade = st.selectbox("🎓 ESCOLARIDADE", ["Fundamental Incompleto", "Fundamental Completo", "Médio Incompleto", "Médio Completo", "Técnico", "Superior Incompleto", "Superior Completo", "Pós-Graduação", "Mestrado", "Doutorado"])
    with c3: setor = st.selectbox("💼 SETOR DE ATIVIDADE", ["Serviços", "Comércio", "Indústria", "Educação", "Saúde", "TI/Tecnologia", "Construção Civil", "Transportes", "Administração Pública", "Outros"])

    st.markdown("---")
    m1, m2 = st.columns(2)
    with m1: mun_moradia = st.selectbox("🏠 MUNICÍPIO (Moradia)", municipios_rmsp, index=municipios_rmsp.index("São Paulo"))
    with m2: dist_moradia = st.selectbox("📍 DISTRITO (Moradia)", distritos_sp, index=distritos_sp.index("Rio Pequeno")) if mun_moradia == "São Paulo" else st.text_input("📍 BAIRRO (Moradia)", "Centro")

    t1, t2, t3 = st.columns(3)
    with t1: mun_trabalho = st.selectbox("🏢 MUNICÍPIO (Trabalho)", municipios_rmsp, index=municipios_rmsp.index("São Paulo"))
    with t2: dist_trabalho = st.selectbox("📍 DISTRITO (Trabalho)", distritos_sp, index=distritos_sp.index("Alto de Pinheiros")) if mun_trabalho == "São Paulo" else st.text_input("📍 BAIRRO (Trabalho)", "Centro")
    with t3: h_dia = st.number_input("⏳ HORAS NO TRECHO (Total Ida/Volta)", value=2.0, step=0.5)

    st.markdown("---")
    st.markdown("### 🚌 CUSTOS DIÁRIOS DE TRANSPORTE (Ida/Volta)")
    tr1, tr2, tr3, tr4, tr5 = st.columns(5)
    with tr1: g_on = st.number_input("🚍 ÔNIBUS (R$)", min_value=0.0)
    with tr2: g_me = st.number_input("🚇 METRÔ (R$)", min_value=0.0)
    with tr3: g_tr = st.number_input("🚆 TREM (R$)", min_value=0.0)
    with tr4: g_ap = st.number_input("🚗 APP (R$)", min_value=0.0)
    with tr5: g_ca = st.number_input("⛽ COMBUSTÍVEL (R$)", min_value=0.0)

    st.markdown("---")
    st.markdown("### 💰 RENDIMENTOS E CUSTO DE VIDA")
    r1, r2, r3 = st.columns(3)
    with r1: sal = st.number_input("💰 SALÁRIO BRUTO (R$)", min_value=0.0)
    with r2: c_vida = st.number_input("🏠 CUSTO DE VIDA (ALUGUEL/COMIDA) (R$) ? (Opcional)", min_value=0.0)
    with r3: dias = st.number_input("📅 DIAS TRABALHADOS/MÊS", value=22)

    submit = st.form_submit_button("EFETUAR DIAGNÓSTICO")

# 4. LÓGICA E RESULTADOS
if submit:
    gasto_d = g_on + g_me + g_tr + g_ap + g_ca
    custo_m = gasto_d * dias
    v_h_nom = sal / 176 if sal > 0 else 0
    h_m = h_dia * dias
    sal_liq_transp = sal - custo_m
    sobra = sal_liq_transp - c_vida
    v_h_re = sal_liq_transp / (176 + h_m) if (176 + h_m) > 0 else 0
    
    valor_tempo_nao_pago = h_m * v_h_nom
    confi = custo_m + valor_tempo_nao_pago
    depre = (1 - (v_h_re / v_h_nom)) * 100 if v_h_nom > 0 else 0

    # VETOR DE FLUXO
    label_moradia = f"{dist_moradia.upper()}" if mun_moradia == mun_trabalho else f"{mun_moradia.upper()} ({dist_moradia.upper()})"
    label_trabalho = f"{dist_trabalho.upper()}" if mun_moradia == mun_trabalho else f"{mun_trabalho.upper()} ({dist_trabalho.upper()})"
    
    st.markdown(f"""
    <div style="background:#000; padding:25px; border:2px solid #E63946; text-align:center; margin: 20px 0;">
        <div style="color:#FFCC00; font-weight:bold; font-size:1.6rem;">
            🏠 {label_moradia} ———▶ 💼 {label_trabalho}
        </div>
        <div style="margin-top:10px; color:#FFCC00; font-size:1.2rem;">{mun_moradia if mun_moradia == mun_trabalho else ""}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<div style="background-color: #E63946; color: white; padding: 15px; text-align: center; font-weight: bold; border-radius: 5px;">🚨 ALERTA DE EXPROPRIAÇÃO MENSAL</div>""", unsafe_allow_html=True)

    # MÉTRICAS CONSOLIDATAS
    st.markdown(f"""
    <div class="report-box">
        <h3 style="margin-top:0; color:#FFCC00;">📋 RESULTADOS</h3>
        <p>• 💹 <b>VALOR DA HORA TRABALHADA:</b> De R$ {v_h_nom:.2f} para <span style="color:#E63946;">R$ {v_h_re:.2f}</span></p>
        <p>• ⏳ <b>TEMPO DE TRABALHO NÃO PAGO:</b> {h_m:.1f}h/mês</p>
        <p>• 💸 <b>VALOR DO CONFISCO (TARIFA + TEMPO NÃO PAGO):</b> R$ {confi:.2f}</p>
        <p>• 💵 <b>SALÁRIO LÍQUIDO DO TRANSPORTE:</b> R$ {sal_liq_transp:.2f}</p>
        <p>• 📉 <b>SOBRA RESIDUAL:</b> R$ {sobra:.2f}</p>
        <p>• 📉 <b>DEPRECIAÇÃO DA FORÇA DE TRABALHO:</b> <span style="color:#E63946;">{depre:.1f}%</span></p>
    </div>
    """, unsafe_allow_html=True)

    # NOTA TÉCNICA
    st.markdown(f"""
    <div style="background-color: #111; padding: 20px; border-left: 5px solid #FFCC00; margin-top: 25px;">
        <b style="color: #FFCC00;">NOTA TÉCNICA:</b><br>
        O "Confisco" reflete o valor total subtraído do rendimento real do trabalhador. 
        Ele soma o gasto direto em tarifas ao valor monetário do tempo de deslocamento (calculado sobre o valor da hora nominal). 
        Consideramos o trecho como "trabalho não pago" pois é um tempo obrigatório para a reprodução da força de trabalho, mas não remunerado.
    </div>
    """, unsafe_allow_html=True)

    # DOWNLOAD
    relatorio = f"DIAGNÓSTICO: {mun_moradia}\nCONFISCO: R$ {confi:.2f}\nTEMPO NÃO PAGO: {h_m:.1f}h"
    st.download_button("📥 BAIXAR NOTA TÉCNICA", relatorio, file_name=f"nota_tecnica.txt")
