import streamlit as st

# 1. SETUP E LIMPEZA RADICAL DE INTERFACE
st.set_page_config(page_title="Calculadora do Trecho", layout="wide")

st.markdown("""
    <style>
    /* 1. ELIMINAÇÃO TOTAL DA FAIXA SUPERIOR E FOOTER */
    header, [data-testid="stHeader"], footer {
        visibility: hidden !important;
        display: none !important;
        height: 0px !important;
    }
    
    /* 2. REAJUSTE DE MARGEM PARA O CONTEÚDO SUBIR */
    .block-container {
        padding-top: 0rem !important;
        margin-top: -50px !important;
    }

    /* 3. FUNDO PRETO ABSOLUTO */
    .stApp { background-color: #000000 !important; }
    
    /* 4. TEXTOS EM AMARELO SEM BORDAS NOS CAMPOS */
    h1, h2, h3, label, p, span { 
        color: #FFCC00 !important; 
        font-family: 'Arial', sans-serif !important;
    }

    /* REMOVENDO BORDAS DOS INPUTS PARA UM LOOK CLEAN */
    div[data-baseweb="input"], div[data-baseweb="select"], .stSelectbox, .stNumberInput {
        border: none !important;
        border-bottom: 1px solid #333 !important; /* Linha discreta apenas embaixo */
        border-radius: 0px !important;
        background-color: #111 !important;
    }
    
    input { color: #FFFFFF !important; }
    div[role="listbox"] { color: #FFFFFF !important; background-color: #111 !important; }

    /* 5. BOTÃO DE IMPACTO (SEMPRE VISÍVEL E SEM CONFLITO) */
    .stButton>button { 
        background-color: #FFCC00 !important; 
        color: #000000 !important; 
        font-weight: 900 !important; 
        width: 100%; 
        height: 3.5em; 
        border: none !important;
        font-size: 1.4rem !important;
        text-transform: uppercase;
        margin-top: 30px !important;
        z-index: 999;
    }
    .stButton>button:hover { background-color: #E63946 !important; color: #FFFFFF !important; }

    /* 6. CAIXA DE RESULTADOS */
    .report-box { 
        background-color: #111; 
        padding: 25px; 
        border-left: 5px solid #FFCC00; 
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CABEÇALHO
st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True) 
col_tit, col_logo = st.columns([4, 1])

with col_tit:
    st.markdown('<h1 style="margin: 0; padding-top: 10px;">CALCULADORA DO TRECHO</h1>', unsafe_allow_html=True)

with col_logo:
    try:
        st.image("logo.png", width=140)
    except:
        st.markdown('<p style="text-align:right; color:#FFCC00;">[LOGO]</p>', unsafe_allow_html=True)

# 3. FRASE DE IMPACTO
st.markdown("""
    <div style="background-color: #FFCC00; color: #000; padding: 20px; text-align: center; font-size: 1.4rem; font-weight: 900; margin: 25px 0;">
        QUANTO DE TEMPO E DE DINHEIRO SÃO CONSUMIDOS NO SEU DESLOCAMENTO DIÁRIO?
    </div>
    """, unsafe_allow_html=True)

# 4. DADOS GEOGRÁFICOS
municipios = [" "] + sorted(["Arujá", "Barueri", "Caieiras", "Cajamar", "Carapicuíba", "Cotia", "Diadema", "Embu das Artes", "Francisco Morato", "Franco da Rocha", "Guarulhos", "Itapevi", "Itaquaquecetuba", "Jandira", "Mairiporã", "Mauá", "Mogi das Cruzes", "Osasco", "Poá", "Ribeirão Pires", "Rio Grande da Serra", "Santana de Parnaíba", "Santo André", "São Bernardo do Campo", "São Caetano do Sul", "São Paulo", "Suzano", "Taboão da Serra"])
distritos = [" "] + sorted(["Água Rasa", "Alto de Pinheiros", "Anhanguera", "Aricanduva", "Artur Alvim", "Barra Funda", "Bela Vista", "Belém", "Bom Retiro", "Brasilândia", "Butantã", "Cachoeirinha", "Cambuci", "Campo Belo", "Campo Grande", "Campo Limpo", "Cangaíba", "Capão Redondo", "Carrão", "Casa Verde", "Cidade Ademar", "Cidade Dutra", "Cidade Líder", "Cidade Tiradentes", "Consolação", "Cursino", "Ermelino Matarazzo", "Freguesia do Ó", "Grajaú", "Guaianases", "Iguatemi", "Ipiranga", "Itaim Bibi", "Itaim Paulista", "Itaquera", "Jabaquara", "Jaçanã", "Jaguara", "Jaguaré", "Jaraguá", "Jardim Ângela", "Jardim Helena", "Jardim Paulista", "Jardim São Luís", "Lapa", "Liberdade", "Limão", "Mandaqui", "Marsilac", "Moema", "Mooca", "Morumbi", "Parelheiros", "Pari", "Parque do Carmo", "Pedreira", "Penha", "Perdizes", "Perus", "Pinheiros", "Pirituba", "Ponte Rasa", "Raposo Tavares", "República", "Rio Pequeno", "Sacomã", "Santa Cecília", "Santana", "Santo Amaro", "São Domingos", "São Lucas", "São Mateus", "São Miguel", "São Rafael", "Sapopemba", "Saúde", "Sé", "Socorro", "Tatuapé", "Tremembé", "Tucuruvi", "Vila Andrade", "Vila Curuçá", "Vila Formosa", "Vila Guilherme", "Vila Jacuí", "Vila Leopoldina", "Vila Maria", "Vila Mariana", "Vila Matilde", "Vila Medeiros", "Vila Prudente", "Vila Sônia"])

# 5. CAMPOS DE ENTRADA
st.markdown("### 👤 PERFIL")
p1, p2, p3 = st.columns(3)
idade = p1.number_input("IDADE", min_value=14, step=1, value=None)
escolaridade = p2.selectbox("ESCOLARIDADE", [" ", "Fundamental", "Médio", "Técnico", "Superior", "Pós-Graduação"])
setor = p3.selectbox("SETOR", [" ", "Serviços", "Comércio", "Indústria", "Educação", "Saúde", "TI", "Construção"])

st.markdown("### 🏠 LOCALIZAÇÃO E TRAJETO")
l1, l2, l3 = st.columns(3)
mun_m = l1.selectbox("MUNICÍPIO (MORADIA)", municipios)
label_m = l1.selectbox("DISTRITO (MORADIA)", distritos) if mun_m == "São Paulo" else mun_m

mun_t = l2.selectbox("MUNICÍPIO (TRABALHO)", municipios)
label_t = l2.selectbox("DISTRITO (TRABALHO)", distritos) if mun_t == "São Paulo" else mun_t

h_dia = l3.number_input("HORAS NO TRECHO (IDA+VOLTA)", min_value=0.0, step=0.5, value=None)

st.markdown("---")
st.markdown("### 💰 ECONOMIA")
e1, e2, e3 = st.columns(3)
sal = e1.number_input("SALÁRIO BRUTO (R$)", min_value=0.0, value=None)
c_vida = e2.number_input("CUSTO DE VIDA (R$)", min_value=0.0, value=None)
dias = e3.number_input("DIAS TRABALHADOS/MÊS", value=22)

st.markdown("### 🚌 TRANSPORTE DIÁRIO (R$)")
g1, g2, g3, g4, g5 = st.columns(5)
g_on = g1.number_input("🚍 ÔNIBUS", min_value=0.0)
g_me = g2.number_input("🚇 METRÔ", min_value=0.0)
g_tr = g3.number_input("🚆 TREM", min_value=0.0)
g_ap = g4.number_input("🚗 APP", min_value=0.0)
g_ca = g5.number_input("⛽ CARRO", min_value=0.0)

# 6. LÓGICA DE DIAGNÓSTICO
if st.button("EFETUAR DIAGNÓSTICO"):
    if sal and h_dia:
        tarifa_m = (g_on + g_me + g_tr + g_ap + g_ca) * dias
        h_m = h_dia * dias
        v_h_nom = sal / 176
        sal_liq_transp = sal - tarifa_m
        v_h_re = sal_liq_transp / (176 + h_m)
        confi = tarifa_m + (h_m * v_h_nom)
        label_sobra = "SOBRA RESIDUAL (PÓS-CUSTO DE VIDA)" if c_vida else "SOBRA RESIDUAL (PÓS-TRANSPORTE)"
        sobra = sal_liq_transp - (c_vida if c_vida else 0)
        depre = (1 - (v_h_re / v_h_nom)) * 100

        st.markdown(f"""
        <div class="report-box">
            <h3 style="margin-top:0; color:#FFCC00;">📋 RESULTADOS</h3>
            <p>• 💹 <b>VALOR DA HORA TRABALHADA:</b> De R$ {v_h_nom:.2f} para <span style="color:#E63946;">R$ {v_h_re:.2f}</span></p>
            <p>• ⏳ <b>TEMPO DE TRABALHO NÃO PAGO:</b> {h_m:.1f}h/mês</p>
            <p>• 💸 <b>VALOR DO CONFISCO (TARIFA + TEMPO NÃO PAGO):</b> R$ {confi:.2f}</p>
            <p>• 💵 <b>SALÁRIO LÍQUIDO (-TRANSPORTE):</b> R$ {sal_liq_transp:.2f}</p>
            <p>• 📉 <b>{label_sobra}:</b> R$ {sobra:.2f}</p>
            <p>• 📉 <b>DEPRECIAÇÃO DA FORÇA DE TRABALHO:</b> <span style="color:#E63946;">{depre:.1f}%</span></p>
        </div>
        """, unsafe_allow_html=True)

        relatorio = f"DIAGNÓSTICO TÉCNICO\\nFLUXO: {label_m} -> {label_t}\\nCONFISCO: R$ {confi:.2f}\\nSALÁRIO LÍQUIDO (-TRANSPORTE): R$ {sal_liq_transp:.2f}\\nDEPRECIAÇÃO: {depre:.1f}%"
        st.download_button("📥 BAIXAR NOTA TÉCNICA", relatorio, file_name="diagnostico_trecho.txt")
    else:
        st.error("Preencha Salário e Horas no Trecho.")
