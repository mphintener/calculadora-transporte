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

# 2. BANCO DE DADOS GEOGRÁFICO
municipios_rmsp = sorted(["Arujá", "Barueri", "Biritiba-Mirim", "Caieiras", "Cajamar", "Carapicuíba", "Cotia", "Diadema", "Embu das Artes", "Embu-Guaçu", "Ferraz de Vasconcelos", "Francisco Morato", "Franco da Rocha", "Guararema", "Guarulhos", "Itapecerica da Serra", "Itapevi", "Itaquaquecetuba", "Jandira", "Juquitiba", "Mairiporã", "Mauá", "Mogi das Cruzes", "Osasco", "Pirapora do Bom Jesus", "Poá", "Ribeirão Pires", "Rio Grande da Serra", "Salesópolis", "Santa Isabel", "Santana de Parnaíba", "Santo André", "São Bernardo do Campo", "São Caetano do Sul", "São Lourenço da Serra", "São Paulo", "Suzano", "Taboão da Serra", "Vargem Grande Paulista"])
distritos_sp = sorted(["Água Rasa", "Alto de Pinheiros", "Anhanguera", "Aricanduva", "Artur Alvim", "Barra Funda", "Bela Vista", "Belém", "Bom Retiro", "Brasilândia", "Butantã", "Cachoeirinha", "Cambuci", "Campo Belo", "Campo Grande", "Campo Limpo", "Cangaíba", "Capão Redondo", "Carrão", "Casa Verde", "Cidade Ademar", "Cidade Dutra", "Cidade Líder", "Cidade Tiradentes", "Consolação", "Cursino", "Ermelino Matarazzo", "Freguesia do Ó", "Grajaú", "Guaianases", "Iguatemi", "Ipiranga", "Itaim Bibi", "Itaim Paulista", "Itaquera", "Jabaquara", "Jaçanã", "Jaguara", "Jaguaré", "Jaraguá", "Jardim Ângela", "Jardim Helena", "Jardim Paulista", "Jardim São Luís", "Lapa", "Liberdade", "Limão", "Mandaqui", "Marsilac", "Moema", "Mooca", "Morumbi", "Parelheiros", "Pari", "Parque do Carmo", "Pedreira", "Penha", "Perdizes", "Perus", "Pinheiros", "Pirituba", "Ponte Rasa", "Raposo Tavares", "República", "Rio Pequeno", "Sacomã", "Santa Cecília", "Santana", "Santo Amaro", "São Domingos", "São Lucas", "São Mateus", "São Miguel", "São Rafael", "Sapopemba", "Saúde", "Sé", "Socorro", "Tatuapé", "Tremembé", "Tucuruvi", "Vila Andrade", "Vila Curuçá", "Vila Formosa", "Vila Guilherme", "Vila Jacuí", "Vila Leopoldina", "Vila Maria", "Vila Mariana", "Vila Matilde", "Vila Medeiros", "Vila Prudente", "Vila Sônia"])

st.title("📊 CALCULADORA DO TRECHO")
st.subheader("Quanto de tempo e de dinheiro são consumidos no seu deslocamento diário?")

# --- ENTRADA DE DADOS FORA DO FORM (Para garantir dinamismo) ---

st.markdown("### 👤 PERFIL")
c1, c2, c3 = st.columns(3)
idade = c1.number_input("👤 IDADE", min_value=14, value=30)
escolaridade = c2.selectbox("🎓 ESCOLARIDADE", ["Fundamental Incompleto", "Fundamental Completo", "Médio Incompleto", "Médio Completo", "Técnico", "Superior Incompleto", "Superior Completo", "Pós-Graduação", "Mestrado", "Doutorado"])
setor = c3.selectbox("💼 SETOR DE ATIVIDADE", ["Serviços", "Comércio", "Indústria", "Educação", "Saúde", "TI/Tecnologia", "Construção Civil", "Transportes", "Administração Pública", "Outros"])

st.markdown("---")
st.markdown("### 🏠 LOCAL DE MORADIA")
m1, m2 = st.columns(2)
mun_moradia = m1.selectbox("MUNICÍPIO (Moradia)", municipios_rmsp, index=municipios_rmsp.index("São Paulo"))
if mun_moradia == "São Paulo":
    dist_moradia = m2.selectbox("DISTRITO (Moradia)", distritos_sp, index=distritos_sp.index("Rio Pequeno"))
else:
    dist_moradia = m2.text_input("BAIRRO/DISTRITO (Moradia)", placeholder="Digite seu bairro")

st.markdown("### 🏢 LOCAL DE TRABALHO")
t1, t2, t3 = st.columns(3)
mun_trabalho = t1.selectbox("MUNICÍPIO (Trabalho)", municipios_rmsp, index=municipios_rmsp.index("São Paulo"))
if mun_trabalho == "São Paulo":
    dist_trabalho = t2.selectbox("DISTRITO (Trabalho)", distritos_sp, index=distritos_sp.index("Alto de Pinheiros"))
else:
    dist_trabalho = t2.text_input("BAIRRO/DISTRITO (Trabalho)", placeholder="Digite o bairro de trabalho")
h_dia = t3.number_input("⏳ HORAS NO TRECHO (Ida/Volta)", value=2.0, step=0.5)

st.markdown("---")
st.markdown("### 🚌 CUSTOS DIÁRIOS E RENDIMENTOS")
tr1, tr2, tr3, tr4, tr5 = st.columns(5)
g_on = tr1.number_input("🚍 ÔNIBUS (R$)", min_value=0.0)
g_me = tr2.number_input("🚇 METRÔ (R$)", min_value=0.0)
g_tr = tr3.number_input("🚆 TREM (R$)", min_value=0.0)
g_ap = tr4.number_input("🚗 APP (R$)", min_value=0.0)
g_ca = tr5.number_input("⛽ CARRO (R$)", min_value=0.0)

r1, r2, r3 = st.columns(3)
sal = r1.number_input("💰 SALÁRIO BRUTO (R$)", min_value=0.0)
c_vida = r2.number_input("🏠 CUSTO DE VIDA (R$)", min_value=0.0, help="Soma de: Aluguel, Comida, Energia, Água e Internet.")
dias = r3.number_input("📅 DIAS TRABALHADOS/MÊS", value=22)

# Botão de ação (fora do form)
if st.button("EFETUAR DIAGNÓSTICO"):
    # LÓGICA DE CÁLCULO
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
    label_m = f"{dist_moradia.upper()}" if mun_moradia == mun_trabalho else f"{mun_moradia.upper()} ({dist_moradia.upper()})"
    label_t = f"{dist_trabalho.upper()}" if mun_moradia == mun_trabalho else f"{mun_trabalho.upper()} ({dist_trabalho.upper()})"
    
    st.markdown(f"""
    <div style="background:#000; padding:25px; border:2px solid #E63946; text-align:center; margin: 20px 0;">
        <div style="color:#FFCC00; font-weight:bold; font-size:1.6rem;">
            🏠 {label_m} ———▶ 💼 {label_t}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<div style="background-color: #E63946; color: white; padding: 15px; text-align: center; font-weight: bold; border-radius: 5px;">🚨 ALERTA DE EXPROPRIAÇÃO MENSAL</div>""", unsafe_allow_html=True)

    # RESULTADOS
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
        O "Confisco" reflete o valor total subtraído do rendimento real do trabalhador. Ele soma o gasto direto em tarifas ao valor monetário do tempo de deslocamento (calculado sobre o valor da hora nominal). Consideramos o trecho como "trabalho não pago" pois é um tempo obrigatório para a reprodução da força de trabalho, mas não remunerado.
    </div>
    """, unsafe_allow_html=True)

    relatorio = f"DIAGNÓSTICO: {mun_moradia}\nCONFISCO: R$ {confi:.2f}\nTEMPO NÃO PAGO: {h_m:.1f}h"
    st.download_button("📥 BAIXAR NOTA TÉCNICA", relatorio, file_name="diagnostico_trecho.txt")
