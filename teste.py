import streamlit as st

# 1. CONFIGURAÇÃO E IDENTIDADE VISUAL (LIMPEZA TOTAL)
st.set_page_config(page_title="Calculadora do Trecho", layout="wide")

st.markdown("""
    <style>
    /* MATA A FAIXA AMARELA E O HEADER NATIVO DO STREAMLIT */
    header, [data-testid="stHeader"] {visibility: hidden; height: 0%; position: absolute;}
    footer {visibility: hidden;}
    .block-container {padding-top: 1rem !important; padding-bottom: 1rem !important;}
    
    /* FUNDO PRETO ABSOLUTO */
    .stApp { background-color: #000000; color: #FFFFFF; }
    h1, h2, h3, label, p, span { color: #FFCC00 !important; font-family: 'Arial', sans-serif; }
    
    /* TÍTULO À ESQUERDA */
    .titulo-principal {
        color: #FFCC00;
        font-size: 2.2rem !important;
        font-weight: 900;
        margin: 0;
        padding: 0;
    }

    /* INPUTS COM BORDA AMARELA */
    input, select, .stSelectbox, div[data-baseweb="input"] {
        background-color: #111 !important;
        color: white !important;
        border: 1px solid #FFCC00 !important;
    }

    /* BOTÃO IMPACTANTE */
    .stButton>button { 
        background-color: #FFCC00 !important; 
        color: #000000 !important; 
        font-weight: 900 !important; 
        width: 100%; 
        height: 3.5em; 
        border: none; 
        font-size: 1.4rem !important;
        text-transform: uppercase;
    }
    .stButton>button:hover { background-color: #E63946 !important; color: #FFFFFF !important; }

    /* CAIXA DE RESULTADOS SEM FANTASMAS */
    .report-box { 
        background-color: #111 !important; 
        padding: 25px; 
        border: 3px solid #FFCC00; 
        border-radius: 10px; 
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CABEÇALHO: TÍTULO ESQUERDA | LOGO DIREITA
t1, t2 = st.columns([3, 1])
with t1:
    st.markdown('<h1 class="titulo-principal">CALCULADORA DO TRECHO</h1>', unsafe_allow_html=True)
with t2:
    # Aumentei para 150 para não ficar pequeno demais
    try:
        st.image("logo.png", width=150)
    except:
        st.write("⚠️ Logo não encontrado")

# 3. FRASE DE IMPACTO (O DESTAQUE CENTRAL)
st.markdown(f"""
    <div style="
        background-color: #FFCC00; 
        color: #000000; 
        padding: 20px; 
        border-radius: 10px; 
        text-align: center; 
        font-size: 1.5rem; 
        font-weight: 900; 
        margin: 20px 0;
        border: 5px solid #E63946;
        text-transform: uppercase;
    ">
        Quanto de tempo e de dinheiro são consumidos no seu deslocamento diário?
    </div>
    """, unsafe_allow_html=True)

# 4. BANCO DE DADOS GEOGRÁFICO
municipios_rmsp = [" "] + sorted(["Arujá", "Barueri", "Biritiba-Mirim", "Caieiras", "Cajamar", "Carapicuíba", "Cotia", "Diadema", "Embu das Artes", "Embu-Guaçu", "Ferraz de Vasconcelos", "Francisco Morato", "Franco da Rocha", "Guararema", "Guarulhos", "Itapecerica da Serra", "Itapevi", "Itaquaquecetuba", "Jandira", "Juquitiba", "Mairiporã", "Mauá", "Mogi das Cruzes", "Osasco", "Pirapora do Bom Jesus", "Poá", "Ribeirão Pires", "Rio Grande da Serra", "Salesópolis", "Santa Isabel", "Santana de Parnaíba", "Santo André", "São Bernardo do Campo", "São Caetano do Sul", "São Lourenço da Serra", "São Paulo", "Suzano", "Taboão da Serra", "Vargem Grande Paulista"])
distritos_sp = [" "] + sorted(["Água Rasa", "Alto de Pinheiros", "Anhanguera", "Aricanduva", "Artur Alvim", "Barra Funda", "Bela Vista", "Belém", "Bom Retiro", "Brasilândia", "Butantã", "Cachoeirinha", "Cambuci", "Campo Belo", "Campo Grande", "Campo Limpo", "Cangaíba", "Capão Redondo", "Carrão", "Casa Verde", "Cidade Ademar", "Cidade Dutra", "Cidade Líder", "Cidade Tiradentes", "Consolação", "Cursino", "Ermelino Matarazzo", "Freguesia do Ó", "Grajaú", "Guaianases", "Iguatemi", "Ipiranga", "Itaim Bibi", "Itaim Paulista", "Itaquera", "Jabaquara", "Jaçanã", "Jaguara", "Jaguaré", "Jaraguá", "Jardim Ângela", "Jardim Helena", "Jardim Paulista", "Jardim São Luís", "Lapa", "Liberdade", "Limão", "Mandaqui", "Marsilac", "Moema", "Mooca", "Morumbi", "Parelheiros", "Pari", "Parque do Carmo", "Pedreira", "Penha", "Perdizes", "Perus", "Pinheiros", "Pirituba", "Ponte Rasa", "Raposo Tavares", "República", "Rio Pequeno", "Sacomã", "Santa Cecília", "Santana", "Santo Amaro", "São Domingos", "São Lucas", "São Mateus", "São Miguel", "São Rafael", "Sapopemba", "Saúde", "Sé", "Socorro", "Tatuapé", "Tremembé", "Tucuruvi", "Vila Andrade", "Vila Curuçá", "Vila Formosa", "Vila Guilherme", "Vila Jacuí", "Vila Leopoldina", "Vila Maria", "Vila Mariana", "Vila Matilde", "Vila Medeiros", "Vila Prudente", "Vila Sônia"])

# 5. ENTRADA DE DADOS
st.markdown("### 👤 PERFIL")
p1, p2, p3 = st.columns(3)
idade = p1.number_input("👤 IDADE", min_value=14, value=None)
escolaridade = p2.selectbox("🎓 ESCOLARIDADE", ["Fundamental", "Médio", "Técnico", "Superior", "Pós/Mestrado/Doutorado"])
setor = p3.selectbox("💼 SETOR", ["Serviços", "Comércio", "Indústria", "Educação", "Saúde", "TI", "Construção", "Outros"])

st.markdown("---")
st.markdown("### 🏠 LOCALIZAÇÃO")
m1, m2 = st.columns(2)
mun_moradia = m1.selectbox("MUNICÍPIO (Moradia)", municipios_rmsp)
if mun_moradia == "São Paulo":
    dist_moradia = m2.selectbox("DISTRITO (Moradia)", distritos_sp)
else:
    dist_moradia = m2.text_input("BAIRRO/DISTRITO (Moradia)")

t1_loc, t2_loc, t3_loc = st.columns(3)
mun_trabalho = t1_loc.selectbox("MUNICÍPIO (Trabalho)", municipios_rmsp)
if mun_trabalho == "São Paulo":
    dist_trabalho = t2_loc.selectbox("DISTRITO (Trabalho)", distritos_sp)
else:
    dist_trabalho = t2_loc.text_input("BAIRRO (Trabalho)")
h_dia = t3_loc.number_input("⏳ HORAS NO TRECHO (Ida/Volta)", value=None, step=0.5)

st.markdown("---")
st.markdown("### 💰 ECONOMIA")
r1, r2, r3 = st.columns(3)
sal = r1.number_input("💰 SALÁRIO BRUTO (R$)", value=None)
c_vida = r2.number_input("🏠 CUSTO DE VIDA (R$)", value=None)
dias = r3.number_input("📅 DIAS TRABALHADOS/MÊS", value=22)

st.markdown("### 🚌 GASTOS DIÁRIOS")
tr1, tr2, tr3, tr4, tr5 = st.columns(5)
g_on = tr1.number_input("🚍 ÔNIBUS", value=0.0)
g_me = tr2.number_input("🚇 METRÔ", value=0.0)
g_tr = tr3.number_input("🚆 TREM", value=0.0)
g_ap = tr4.number_input("🚗 APP", value=0.0)
g_ca = tr5.number_input("⛽ CARRO", value=0.0)

# 6. LÓGICA E RESULTADOS
if st.button("EFETUAR DIAGNÓSTICO"):
    if not mun_moradia.strip() or not mun_trabalho.strip() or sal is None or h_dia is None:
        st.error("⚠️ Preencha os campos obrigatórios (Municípios, Horas e Salário).")
    else:
        gasto_d = g_on + g_me + g_tr + g_ap + g_ca
        custo_m = gasto_d * dias
        v_h_nom = sal / 176 if sal > 0 else 0
        h_m = h_dia * dias
        sal_liq_transp = sal - custo_m
        sobra = sal_liq_transp - (c_vida or 0)
        v_h_re = sal_liq_transp / (176 + h_m) if (176 + h_m) > 0 else 0
        valor_tempo_nao_pago = h_m * v_h_nom
        confi = custo_m + valor_tempo_nao_pago
        depre = (1 - (v_h_re / v_h_nom)) * 100 if v_h_nom > 0 else 0
        label_sobra = "SOBRA RESIDUAL (PÓS-CUSTO DE VIDA)" if (c_vida and c_vida > 0) else "SOBRA RESIDUAL (PÓS-TRANSPORTE)"

        st.markdown(f"""
        <div class="report-box">
            <h3 style="margin-top:0;">📋 DIAGNÓSTICO DA EXPROPRIAÇÃO</h3>
            <p>• 💹 <b>VALOR DA HORA TRABALHADA:</b> De R$ {v_h_nom:.2f} para <span style="color:#E63946;">R$ {v_h_re:.2f}</span></p>
            <p>• ⏳ <b>TEMPO DE TRABALHO NÃO PAGO:</b> {h_m:.1f}h / mês</p>
            <p>• 💸 <b>VALOR DO CONFISCO (PASSAGEM + TEMPO):</b> R$ {confi:.2f}</p>
            <p>• 💵 <b>SALÁRIO LÍQUIDO (-TRANSPORTE):</b> R$ {sal_liq_transp:.2f}</p>
            <p>• 📉 <b>{label_sobra}:</b> R$ {sobra:.2f}</p>
            <p>• 📉 <b>DEPRECIAÇÃO DA FORÇA DE TRABALHO:</b> <span style="color:#E63946;">{depre:.1f}%</span></p>
        </div>
        """, unsafe_allow_html=True)
        relatorio = f"DIAGNÓSTICO TÉCNICO\nFLUXO: {label_m} -> {label_t}\nCONFISCO: R$ {confi:.2f}\nSALÁRIO LÍQUIDO (-TRANSPORTE): R$ {sal_liq_transp:.2f}"
        st.download_button("📥 BAIXAR NOTA TÉCNICA", relatorio, file_name="diagnostico_trecho.txt")
