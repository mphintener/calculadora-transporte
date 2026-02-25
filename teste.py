import streamlit as st

# 1. SETUP E ESTILO
st.set_page_config(page_title="Diagnóstico de Expropriação", layout="wide")

st.markdown("""
    <style>
    header { visibility: hidden; height: 0px; }
    .stApp { background-color: #000000 !important; }
    h1, h2, h3, label, p, span { color: #FFCC00 !important; font-family: 'Arial Black', sans-serif !important; }
    div[data-baseweb="input"], .stNumberInput, .stTextInput, .stSelectbox {
        border: none !important; border-bottom: 2px solid #333 !important; background-color: transparent !important;
    }
    input { color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; }
    .stButton>button { 
        background-color: #FFCC00 !important; color: #000 !important; font-weight: 900 !important; 
        width: 100%; border: 4px solid #E63946 !important; height: 4em; text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. LISTAS COMPLETAS (RMSP e Distritos SP)
municipios_rmsp = sorted(["Arujá", "Barueri", "Biritiba-Mirim", "Caieiras", "Cajamar", "Carapicuíba", "Cotia", "Diadema", "Embu das Artes", "Embu-Guaçu", "Ferraz de Vasconcelos", "Francisco Morato", "Franco da Rocha", "Guararema", "Guarulhos", "Itapecerica da Serra", "Itapevi", "Itaquaquecetuba", "Jandira", "Juquitiba", "Mairiporã", "Mauá", "Mogi das Cruzes", "Osasco", "Pirapora do Bom Jesus", "Poá", "Ribeirão Pires", "Rio Grande da Serra", "Salesópolis", "Santa Isabel", "Santana de Parnaíba", "Santo André", "São Bernardo do Campo", "São Caetano do Sul", "São Lourenço da Serra", "São Paulo", "Suzano", "Taboão da Serra", "Vargem Grande Paulista"])
distritos_sp = sorted(["Água Rasa", "Alto de Pinheiros", "Anhanguera", "Aricanduva", "Artur Alvim", "Barra Funda", "Bela Vista", "Belém", "Bom Retiro", "Brasilândia", "Butantã", "Cachoeirinha", "Cambuci", "Campo Belo", "Campo Grande", "Campo Limpo", "Cangaíba", "Capão Redondo", "Carrão", "Casa Verde", "Cidade Ademar", "Cidade Dutra", "Cidade Líder", "Cidade Tiradentes", "Consolação", "Cursino", "Ermelino Matarazzo", "Freguesia do Ó", "Grajaú", "Guaianases", "Ipiranga", "Itaim Bibi", "Itaim Paulista", "Itaquera", "Jabaquara", "Jaçanã", "Jaguara", "Jaguare", "Jaraguá", "Jardim Ângela", "Jardim Helena", "Jardim Paulista", "Jardim São Luís", "José Bonifácio", "Lajeado", "Lapa", "Liberdade", "Limão", "Mandaqui", "Marsilac", "Moema", "Mooca", "Morumbi", "Parelheiros", "Pari", "Parque do Carmo", "Passagem", "Pedreira", "Penha", "Perdizes", "Perus", "Pinheiros", "Pirituba", "Ponte Rasa", "Raposo Tavares", "República", "Rio Pequeno", "Sacomã", "Santa Cecília", "Santana", "Santo Amaro", "São Domingos", "São Lucas", "São Mateus", "São Miguel", "São Rafael", "Sapopemba", "Saúde", "Sé", "Socorro", "Tatuapé", "Tremembé", "Tucuruvi", "Vila Andrade", "Vila Curuçá", "Vila Formosa", "Vila Guilherme", "Vila Jacuí", "Vila Leopoldina", "Vila Maria", "Vila Mariana", "Vila Matilde", "Vila Medeiros", "Vila Prudente", "Vila Sônia"])

# 3. INTERFACE
st.title("⚖️ DIAGNÓSTICO DE EXPROPRIAÇÃO URBANA")

st.markdown("### 🏠 LOCALIZAÇÃO")
c1, c2, c3, c4 = st.columns(4)
m_mun = c1.selectbox("MUNICÍPIO (Moradia)", municipios_rmsp, index=municipios_rmsp.index("São Paulo"), key="m1")
m_loc = c2.selectbox("DISTRITO", distritos_sp, key="m2") if m_mun == "São Paulo" else c2.text_input("BAIRRO", key="m3")
t_mun = c3.selectbox("MUNICÍPIO (Trabalho)", municipios_rmsp, index=municipios_rmsp.index("São Paulo"), key="t1")
t_loc = c4.selectbox("DISTRITO ", distritos_sp, key="t2") if t_mun == "São Paulo" else c4.text_input("BAIRRO ", key="t3")

st.markdown("---")
st.markdown("### 💰 RENDIMENTOS E TEMPO")
r1, r2, r3, r4 = st.columns(4)
salario = r1.number_input("SALÁRIO BRUTO (R$)", min_value=0.0, key="s1")
dias = r2.number_input("DIAS TRABALHADOS/MÊS", value=22, key="d1")
h_dia = r3.number_input("HORAS NO TRECHO (Ida+Volta)", value=2.0, key="h1")
c_vida = r4.number_input("CUSTO DE VIDA (R$)", min_value=0.0, key="cv1")

st.markdown("#### 🚌 CUSTOS DIÁRIOS DE TRANSPORTE")
g1, g2, g3, g4, g5 = st.columns(5)
on = g1.number_input("🚌 ÔNIBUS", key="on")
me = g2.number_input("🚇 METRÔ", key="me")
tr = g3.number_input("🚆 TREM", key="tr")
ap = g4.number_input("🚗 APP", key="ap")
ca = g5.number_input("⛽ CARRO", key="ca")

# 4. CÁLCULOS E RESULTADOS
if st.button("GERAR DIAGNÓSTICO CRÍTICO"):
    gasto_mensal = (on + me + tr + ap + ca) * dias
    sal_pos_transp = salario - gasto_mensal
    h_trecho_mes = h_dia * dias
    
    v_h_nominal = salario / 176 if salario > 0 else 0
    v_h_real = sal_pos_transp / (176 + h_trecho_mes) if salario > 0 else 0
    depreciacao = (1 - (v_h_real / v_h_nominal)) * 100 if v_h_nominal > 0 else 0
    confisco = gasto_mensal + (h_trecho_mes * v_h_nominal)
    
    # Lógica solicitada: Sobra Dinâmica
    label_sobra = "SOBRA RESIDUAL (PÓS-CUSTO DE VIDA)" if c_vida > 0 else "SOBRA RESIDUAL (PÓS-TRANSPORTE)"
    valor_sobra = sal_pos_transp - c_vida

    st.markdown(f"""
    <div style="background:#111; padding:30px; border:5px solid #E63946;">
        <h2 style="color:#FFCC00; text-align:center;">DIAGNÓSTICO DA EXPROPRIAÇÃO</h2>
        <div style="text-align:center; border: 2px solid #FFCC00; padding:15px; background:#000; margin-bottom:20px;">
            <p style="color:#FFCC00; margin:0;">{label_sobra}</p>
            <h1 style="color:#FFF; font-size:3rem; margin:0;">R$ {valor_sobra:.2f}</h1>
        </div>
        <p>⚠️ <b>VALOR HORA NOMINAL:</b> R$ {v_h_nominal:.2f}</p>
        <p style="color:#E63946;">⚠️ <b>VALOR HORA REAL:</b> R$ {v_h_real:.2f}</p>
        <p>⚠️ <b>DEPRECIAÇÃO DA FORÇA DE TRABALHO:</b> {depreciacao:.1f}%</p>
        <p style="color:#AAA; font-style: italic;">* O tempo de deslocamento constitui uma jornada de trabalho invisível e não paga.</p>
    </div>
    """, unsafe_allow_html=True)

    # 5. NOTA TÉCNICA
    nota_tecnica = f"""NOTA TÉCNICA: DIAGNÓSTICO DE EXPROPRIAÇÃO URBANA
--------------------------------------------------
TRECHO: {m_loc} -> {t_loc}

O tempo de deslocamento ({h_trecho_mes} horas/mês) é TEMPO DE TRABALHO NÃO PAGO.
{label_sobra}: R$ {valor_sobra:.2f}
Depreciação da Hora de Vida: {depreciacao:.1f}%
--------------------------------------------------"""
    st.download_button("📩 BAIXAR NOTA TÉCNICA", nota_tecnica, file_name="diagnostico.txt")
