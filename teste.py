import streamlit as st

# 1. SETUP E LIMPEZA RADICAL DE INTERFACE
st.set_page_config(page_title="Calculadora do Trecho", layout="wide")

st.markdown("""
    <style>
    /* ELIMINAÇÃO TOTAL DA FAIXA SUPERIOR */
    header, [data-testid="stHeader"], .st-emotion-cache-18ni7ap {
        visibility: hidden !important;
        display: none !important;
        height: 0px !important;
    }
    
    /* CONTEÚDO NO TOPO ABSOLUTO */
    .block-container {
        padding-top: 0rem !important;
        margin-top: -60px !important;
    }

    /* IDENTIDADE VISUAL: PRETO, AMARELO E VERMELHO */
    .stApp { background-color: #000000 !important; }
    
    h1, h2, h3, label, p, span { 
        color: #FFCC00 !important; 
        font-family: 'Arial Black', sans-serif !important;
    }

    /* CAMPOS SEM BORDAS - APENAS LINHA INFERIOR DISCRETA */
    div[data-baseweb="input"], div[data-baseweb="select"], .stSelectbox, .stNumberInput {
        border: none !important;
        border-bottom: 1px solid #333 !important;
        border-radius: 0px !important;
        background-color: #111 !important;
    }
    
    input { color: #FFFFFF !important; }
    div[role="listbox"] { color: #FFFFFF !important; background-color: #111 !important; }

    /* BOTÃO DE IMPACTO */
    .stButton>button { 
        background-color: #FFCC00 !important; 
        color: #000000 !important; 
        font-weight: 900 !important; 
        width: 100%; 
        height: 3.5em; 
        border: 4px solid #E63946 !important;
        font-size: 1.4rem !important;
        text-transform: uppercase;
        margin-top: 30px !important;
    }
    .stButton>button:hover { background-color: #E63946 !important; color: #FFFFFF !important; }

    .report-box { 
        background-color: #111; padding: 25px; border-left: 5px solid #FFCC00; border-radius: 0px; margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. BANCO DE DADOS GEOGRÁFICO
municipios = [" "] + sorted(["Arujá", "Barueri", "Biritiba-Mirim", "Caieiras", "Cajamar", "Carapicuíba", "Cotia", "Diadema", "Embu das Artes", "Embu-Guaçu", "Ferraz de Vasconcelos", "Francisco Morato", "Franco da Rocha", "Guararema", "Guarulhos", "Itapecerica da Serra", "Itapevi", "Itaquaquecetuba", "Jandira", "Juquitiba", "Mairiporã", "Mauá", "Mogi das Cruzes", "Osasco", "Pirapora do Bom Jesus", "Poá", "Ribeirão Pires", "Rio Grande da Serra", "Salesópolis", "Santa Isabel", "Santana de Parnaíba", "Santo André", "São Bernardo do Campo", "São Caetano do Sul", "São Lourenço da Serra", "São Paulo", "Suzano", "Taboão da Serra", "Vargem Grande Paulista"])

distritos = [" "] + sorted(["Água Rasa", "Alto de Pinheiros", "Anhanguera", "Aricanduva", "Artur Alvim", "Barra Funda", "Bela Vista", "Belém", "Bom Retiro", "Brasilândia", "Butantã", "Cachoeirinha", "Cambuci", "Campo Belo", "Campo Grande", "Campo Limpo", "Cangaíba", "Capão Redondo", "Carrão", "Casa Verde", "Cidade Ademar", "Cidade Dutra", "Cidade Líder", "Cidade Tiradentes", "Consolação", "Cursino", "Ermelino Matarazzo", "Freguesia do Ó", "Grajaú", "Guaianases", "Iguatemi", "Ipiranga", "Itaim Bibi", "Itaim Paulista", "Itaquera", "Jabaquara", "Jaçanã", "Jaguara", "Jaguaré", "Jaraguá", "Jardim Ângela", "Jardim Helena", "Jardim Paulista", "Jardim São Luís", "Lapa", "Liberdade", "Limão", "Mandaqui", "Marsilac", "Moema", "Mooca", "Morumbi", "Parelheiros", "Pari", "Parque do Carmo", "Pedreira", "Penha", "Perdizes", "Perus", "Pinheiros", "Pirituba", "Ponte Rasa", "Raposo Tavares", "República", "Rio Pequeno", "Sacomã", "Santa Cecília", "Santana", "Santo Amaro", "São Domingos", "São Lucas", "São Mateus", "São Miguel", "São Rafael", "Sapopemba", "Saúde", "Sé", "Socorro", "Tatuapé", "Tremembé", "Tucuruvi", "Vila Andrade", "Vila Curuçá", "Vila Formosa", "Vila Guilherme", "Vila Jacuí", "Vila Leopoldina", "Vila Maria", "Vila Mariana", "Vila Matilde", "Vila Medeiros", "Vila Prudente", "Vila Sônia"])

# 3. CABEÇALHO
st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True) 
c1, c2 = st.columns([4, 1])
with c1:
    st.markdown('<h1 style="margin: 0;">CALCULADORA DO TRECHO</h1>', unsafe_allow_html=True)
with c2:
    try: st.image("logo.png", width=150)
    except: st.markdown('<p style="text-align:right;">[LOGO]</p>', unsafe_allow_html=True)

# 4. FRASE DE IMPACTO
st.markdown("""
    <div style="background-color: #FFCC00; color: #000; padding: 20px; text-align: center; font-size: 1.4rem; font-weight: 900; margin: 25px 0; border: 4px solid #E63946;">
        Quanto de tempo e de dinheiro são consumidos no seu deslocamento diário?
    </div>
    """, unsafe_allow_html=True)
# 6. ENTRADA DE DADOS: PERFIL DO USUÁRIO (RESTAURADO)
st.markdown("### 👤 PERFIL")
p1, p2, p3 = st.columns(3)
idade = p1.number_input("IDADE", min_value=14, step=1, value=None)
escolaridade = p2.selectbox("ESCOLARIDADE", ["Fundamental Incompleto", "Fundamental Completo", "Médio Incompleto", "Médio Completo", "Técnico", "Superior Incompleto", "Superior Completo", "Pós-Graduação"])
setor = p3.selectbox("SETOR DE ATIVIDADE", ["Comércio", "Construção Civil", "Educação", "Indústria", "Serviços", "Saúde", "Outros"])

# 7. LOCALIZAÇÃO (MORADIA E TRABALHO)
# =========================================================
st.markdown("---")
st.markdown("### 🏠 LOCAL DE MORADIA")
m1, m2 = st.columns(2)
mun_moradia = m1.stselectbox("MUNICÍPIO (Moradia)", municipios, key="mun_mor_final")

if mun_moradia == "São Paulo":
    dist_moradia = m2.stselectbox("DISTRITO (Moradia)", distritos, key="dist_mor_sel")
else:
    dist_moradia = m2.text_input("BAIRRO/DISTRITO (Moradia)", placeholder="Digite seu bairro", key="dist_mor_txt")

st.markdown("### 💼 LOCAL DE TRABALHO")
t1, t2, t3 = st.columns(3)
mun_trabalho = t1.setselectbox("MUNICÍPIO (Trabalho)", municipios, key="mun_trab_final")

if mun_trabalho == "São Paulo":
    dist_trabalho = t2.setselectbox("DISTRITO (Trabalho)", distritos, key="dist_trab_sel")
else:
    dist_trabalho = t2.text_input("BAIRRO/DISTRITO (Trabalho)", placeholder="Digite o bairro", key="dist_trab_txt")

h_dia = t3.number_input("HORAS NO TRECHO (Ida/Volta)", value=2.0, step=0.5)
st.markdown("---")
st.markdown("### 💰 RENDIMENTO E CUSTO")
e1, e2, e3 = st.columns(3)
sal = e1.number_input("SALÁRIO BRUTO (R$)", min_value=0.0, value=None)
c_vida = e2.number_input("🏠 CUSTO DE VIDA (R$)", min_value=0.0, help="Soma de: Aluguel, Comida, Energia, Água, Internet")
dias = e3.number_input("DIAS TRABALHADOS/MÊS", value=22)
st.markdown("### 🚌 TRANSPORTE DIÁRIO (IDA/VOLTA) (R$)")
g1, g2, g3, g4, g5 = st.columns(5)
g_on = g1.number_input("🚍 ÔNIBUS", min_value=0.0)
g_me = g2.number_input("🚇 METRÔ", min_value=0.0)
g_tr = g3.number_input("🚆 TREM", min_value=0.0)
g_ap = g4.number_input("🚗 APP", min_value=0.0)
g_ca = g5.number_input("⛽ CARRO/COMBUSTÍVEL", min_value=0.0)

   # Certifique-se de que este bloco está EXATAMENTE assim, com as aspas triplas no início e no fim
# 1. ESTILO DO BOTÃO E ELIMINAÇÃO DE FAIXAS
st.markdown("""
    <style>
    /* MATA O HEADER E A DECORAÇÃO COLORIDA */
    header, [data-testid="stHeader"], [data-testid="stDecoration"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* FORMATAÇÃO DO BOTÃO EM NEGRITO EXTREMO */
    div.stButton > button {
        opacity: 1 !important;
        background-color: #FFCC00 !important;
        color: #000000 !important;
        font-weight: 900 !important;
        font-family: 'Arial Black', sans-serif !important;
        text-transform: uppercase;
        width: 100% !important;
        height: 3.5em !important;
        border: 4px solid #E63946 !important;
        margin-top: 30px !important;
    }

    /* TEXTO INTERNO DO BOTÃO */
    div.stButton > button p {
        color: #000000 !important;
        font-weight: 900 !important;
    }
    </style>
    """, unsafe_allow_html=True)
   
# 8. DIAGNÓSTICO
if st.button("GERAR DIAGNÓSTICO"):
    # PROTEÇÃO: Verifica se as variáveis foram preenchidas e são maiores que zero
    st.warning("⚠️ Por favor, preencha os campos de SALÁRIO, GASTOS COM TRANSPORTE E HORAS NO TRECHO para continuar")
    if (salario and h_dia and salario > 0):
        # --- CÁLCULOS (SÓ OCORREM SE OS DADOS ESTIVEREM LÁ) ---
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
            <h3 style="margin-top:0;">📋 RESULTADOS TÉCNICOS</h3>
            <p>• 💹 <b>VALOR DA HORA TRABALHADA:</b> De R$ {v_h_nom:.2f} para <span style="color:#E63946;">R$ {v_h_re:.2f}</span></p>
            <p>• ⏳ <b>TEMPO DE TRABALHO NÃO PAGO:</b> {h_m:.1f}h/mês</p>
            <p>• 💸 <b>VALOR DO CONFISCO (TARIFA + TEMPO NÃO PAGO):</b> R$ {confi:.2f}</p>
            <p>• 💵 <b>SALÁRIO LÍQUIDO (-TRANSPORTE):</b> R$ {sal_liq_transp:.2f}</p>
            <p>• 📉 <b>{label_sobra}:</b> R$ {sobra:.2f}</p>
            <p>• 📉 <b>DEPRECIAÇÃO DA FORÇA DE TRABALHO:</b> <span style="color:#E63946;">{depre:.1f}%</span></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background-color: #111; padding: 20px; border-left: 5px solid #E63946; margin-top: 25px; color: #EEE;">
            <b style="color: #FFCC00;">NOTA TÉCNICA:</b><br>
            Consideramos o trecho como "trabalho não pago". O confisco de R$ {confi:.2f} representa a perda real do valor da sua força de trabalho devido ao tempo e custo de mobilidade.
        </div>
        """, unsafe_allow_html=True)

        relatorio = f"DIAGNÓSTICO TÉCNICO\\nFLUXO: {label_m} -> {label_t}\\nCONFISCO: R$ {confi:.2f}\\nDEPRECIAÇÃO: {depre:.1f}%"
        st.download_button("📥 BAIXAR NOTA TÉCNICA", relatorio, file_name="diagnostico_trecho.txt")
    else:
        st.error("Preencha Salário e Horas no Trecho.")
