import streamlit as st
# 1. IDENTIDADE VISUAL E CONFIGURAÇÃO (CSS ULTRA REFORÇADO)
st.set_page_config(page_title="Calculadora do Trecho", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    
    /* Proteção do Cabeçalho contra faixas do sistema */
    .main-header-container {
        padding-top: 40px !important;
        margin-bottom: 20px;
        position: relative;
        z-index: 9999;
    }
    
    h1 { color: #FFCC00 !important; font-family: 'Arial', sans-serif; font-weight: 800; text-align: center; }
    .subheader-text { color: #FFCC00 !important; text-align: center; font-size: 1.2rem; margin-bottom: 40px; }

    .stButton>button { 
        background-color: #FFCC00 !important; 
        color: #000000 !important; 
        font-weight: bold !important; 
        width: 100%; 
        border-radius: 5px; 
        height: 4.5em; 
        border: 2px solid #FFCC00;
        font-size: 1.4rem !important;
        margin-top: 20px;
        box-shadow: 0px 5px 15px rgba(255, 204, 0, 0.3);
    }
    .stButton>button:hover { background-color: #E63946 !important; color: #FFFFFF !important; border-color: #E63946; }

    .report-box { background:#111; padding:30px; border:2px solid #FFCC00; border-radius:10px; margin-top:20px; }
    label, p { color: #FFCC00 !important; font-weight: bold; }
    input, select, .stSelectbox { background-color: #111 !important; color: white !important; border: 1px solid #444 !important; }
    
    .block-container { padding-top: 1rem !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. BANCO DE DADOS GEOGRÁFICO
municipios_rmsp = [" "] + sorted(["Arujá", "Barueri", "Biritiba-Mirim", "Caieiras", "Cajamar", "Carapicuíba", "Cotia", "Diadema", "Embu das Artes", "Embu-Guaçu", "Ferraz de Vasconcelos", "Francisco Morato", "Franco da Rocha", "Guararema", "Guarulhos", "Itapecerica da Serra", "Itapevi", "Itaquaquecetuba", "Jandira", "Juquitiba", "Mairiporã", "Mauá", "Mogi das Cruzes", "Osasco", "Pirapora do Bom Jesus", "Poá", "Ribeirão Pires", "Rio Grande da Serra", "Salesópolis", "Santa Isabel", "Santana de Parnaíba", "Santo André", "São Bernardo do Campo", "São Caetano do Sul", "São Lourenço da Serra", "São Paulo", "Suzano", "Taboão da Serra", "Vargem Grande Paulista"])
distritos_sp = [" "] + sorted(["Água Rasa", "Alto de Pinheiros", "Anhanguera", "Aricanduva", "Artur Alvim", "Barra Funda", "Bela Vista", "Belém", "Bom Retiro", "Brasilândia", "Butantã", "Cachoeirinha", "Cambuci", "Campo Belo", "Campo Grande", "Campo Limpo", "Cangaíba", "Capão Redondo", "Carrão", "Casa Verde", "Cidade Ademar", "Cidade Dutra", "Cidade Líder", "Cidade Tiradentes", "Consolação", "Cursino", "Ermelino Matarazzo", "Freguesia do Ó", "Grajaú", "Guaianases", "Iguatemi", "Ipiranga", "Itaim Bibi", "Itaim Paulista", "Itaquera", "Jabaquara", "Jaçanã", "Jaguara", "Jaguaré", "Jaraguá", "Jardim Ângela", "Jardim Helena", "Jardim Paulista", "Jardim São Luís", "Lapa", "Liberdade", "Limão", "Mandaqui", "Marsilac", "Moema", "Mooca", "Morumbi", "Parelheiros", "Pari", "Parque do Carmo", "Pedreira", "Penha", "Perdizes", "Perus", "Pinheiros", "Pirituba", "Ponte Rasa", "Raposo Tavares", "República", "Rio Pequeno", "Sacomã", "Santa Cecília", "Santana", "Santo Amaro", "São Domingos", "São Lucas", "São Mateus", "São Miguel", "São Rafael", "Sapopemba", "Saúde", "Sé", "Socorro", "Tatuapé", "Tremembé", "Tucuruvi", "Vila Andrade", "Vila Curuçá", "Vila Formosa", "Vila Guilherme", "Vila Jacuí", "Vila Leopoldina", "Vila Maria", "Vila Mariana", "Vila Matilde", "Vila Medeiros", "Vila Prudente", "Vila Sônia"])

st.markdown('<div class="main-header-container"><h1>📊 CALCULADORA DO TRECHO</h1><div class="subheader-text">Quanto de tempo e de dinheiro são consumidos no seu deslocamento diário?</div></div>', unsafe_allow_html=True)

# 6. ENTRADA DE DADOS: PERFIL DO USUÁRIO (RESTAURADO)
st.markdown("### 👤 PERFIL")
p1, p2, p3 = st.columns(3)
idade = p1.number_input("IDADE", min_value=14, step=1, value=None)
escolaridade = p2.selectbox("ESCOLARIDADE", ["Fundamental Incompleto", "Fundamental Completo", "Médio Incompleto", "Médio Completo", "Técnico", "Superior Incompleto", "Superior Completo", "Pós-Graduação"])
setor = p3.selectbox("SETOR DE ATIVIDADE", ["Comércio", "Construção Civil", "Educação", "Indústria", "Serviços", "Saúde", "Outros"])

st.markdown("---")
st.markdown("### 🏠 LOCAL DE MORADIA")
m1, m2 = st.columns(2)
mun_moradia = m1.selectbox("MUNICÍPIO (Moradia)", municipios_rmsp, index=0)
if mun_moradia == "São Paulo":
    dist_moradia = m2.selectbox("DISTRITO (Moradia)", distritos_sp, index=0)
else:
    dist_moradia = m2.text_input("BAIRRO/DISTRITO (Moradia)", placeholder="Digite seu bairro")

st.markdown("### 🏢 LOCAL DE TRABALHO")
t1, t2, t3 = st.columns(3)
mun_trabalho = t1.selectbox("MUNICÍPIO (Trabalho)", municipios_rmsp, index=0)
if mun_trabalho == "São Paulo":
    dist_trabalho = t2.selectbox("DISTRITO (Trabalho)", distritos_sp, index=0)
else:
    dist_trabalho = t2.text_input("BAIRRO/DISTRITO (Trabalho)", placeholder="Digite o bairro de trabalho")
h_dia = t3.number_input("⏳ HORAS NO TRECHO (Ida/Volta)", value=2.0, step=0.5)

st.markdown("---")
st.markdown("### 🚌 CUSTOS DIÁRIOS E RENDIMENTOS")
tr1, tr2, tr3, tr4, tr5 = st.columns(5)
g_on = tr1.number_input("🚍 ÔNIBUS", min_value=0.0)
g_me = tr2.number_input("🚇 METRÔ", min_value=0.0)
g_tr = tr3.number_input("🚆 TREM", min_value=0.0)
g_ap = tr4.number_input("🚗 APP", min_value=0.0)
g_ca = tr5.number_input("⛽ CARRO", min_value=0.0)

r1, r2, r3 = st.columns(3)
sal = r1.number_input("💰 SALÁRIO BRUTO (R$)", min_value=0.0)
c_vida = r2.number_input("🏠 CUSTO DE VIDA (R$)", min_value=0.0, help="Soma de: Aluguel, Comida, Energia, Água e Internet.")
dias = r3.number_input("📅 DIAS TRABALHADOS/MÊS", value=22)

# 4. BOTÃO E LÓGICA
if st.button("EFETUAR DIAGNÓSTICO"):
    if mun_moradia == " " or mun_trabalho == " ":
        st.warning("⚠️ Selecione os municípios para gerar o diagnóstico.")
    else:
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

        # Rótulo Dinâmico para Sobra
        label_sobra = "SOBRA RESIDUAL (DESCONTADO CUSTO DE VIDA)" if c_vida > 0 else "SOBRA RESIDUAL (PÓS-TRANSPORTE)"

        # VETOR DE FLUXO
        d_mor = (dist_moradia or "").upper()
        d_tra = (dist_trabalho or "").upper()
        label_m = d_mor if mun_moradia == mun_trabalho else f"{mun_moradia.upper()} ({d_mor})"
        label_t = d_tra if mun_moradia == mun_trabalho else f"{mun_trabalho.upper()} ({d_tra})"
        
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
            <p>• 💵 <b>SALÁRIO LÍQUIDO (-TRANSPORTE):</b> R$ {sal_liq_transp:.2f}</p>
            <p>• 📉 <b>{label_sobra}:</b> R$ {sobra:.2f}</p>
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

        relatorio = f"DIAGNÓSTICO TÉCNICO\nFLUXO: {label_m} -> {label_t}\nCONFISCO: R$ {confi:.2f}\nSALÁRIO LÍQUIDO (-TRANSPORTE): R$ {sal_liq_transp:.2f}"
        st.download_button("📥 BAIXAR NOTA TÉCNICA", relatorio, file_name="diagnostico_trecho.txt")
