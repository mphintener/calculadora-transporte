import streamlit as st

# 1. SETUP E ESTILO (O "ESCUDO" CONTRA A FAIXA FANTASMA)
st.set_page_config(page_title="Calculadora do Trecho", layout="wide")

st.markdown("""
    <style>
    /* REMOVE A FAIXA BRANCA/FANTASMA DO TOPO */
    header, [data-testid="stHeader"], [data-testid="stStatusWidget"] {
        visibility: hidden !important;
        display: none !important;
        height: 0px !important;
    }
    
    /* FUNDO PRETO ABSOLUTO */
    .stApp { background-color: #000000 !important; }
    
    /* AJUSTE DE ESPAÇO NO TOPO */
    .block-container { 
        padding-top: 1rem !important; 
        margin-top: -40px !important; 
    }

    /* ESTILO DO TÍTULO E FRASE (AMARELO) */
    .titulo-container h1 { 
        color: #FFCC00 !important; 
        font-family: 'Arial Black', sans-serif !important; 
        margin-bottom: 0px !important;
        font-size: 2.2rem !important;
    }
    .frase-impacto {
        color: #FFCC00 !important;
        font-size: 1.1rem !important;
        margin-top: -5px !important;
        margin-bottom: 25px !important;
    }

/* MANTENHA O SEU E ADICIONE ISTO ABAIXO: */
    
    .report-box {
        background-color: #FFFFFF !important;
        padding: 25px;
        border: 5px solid #FFCC00;
        border-radius: 10px;
    }

    /* FORÇA O PRETO EM TUDO QUE ESTIVER DENTRO DA CAIXA DE RESULTADOS */
    .report-box h3, 
    .report-box p, 
    .report-box b, 
    .report-box span,
    .report-box div {
        color: #000000 !important;
    }
    
    /* LABELS EM AMARELO */
    label, p, span { color: #FFCC00 !important; font-weight: bold !important; }

    /* ESTILO DOS CAMPOS (HÍBRIDO) */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border-radius: 4px !important;
    }
    
    .stTextInput input, .stNumberInput input {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-bottom: 2px solid #FFCC00 !important;
        border-radius: 0px !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CABEÇALHO: TÍTULO COM RESPIRO E LOGO REDUZIDO
# Aumentamos a proporção para 4:1 para o logo ficar menor
col_titulo, col_logo = st.columns([4, 1])

with col_titulo:
    # Adicionamos 'padding-top' para descer o título
    st.markdown("""
        <div style="padding-top: 25px;">
            <h1 style="color: #FFCC00 !important; font-family: 'Arial Black', sans-serif !important; margin-bottom: 0px !important; font-size: 2.2rem !important; text-align: left !important;">
                ⚖️ CALCULADORA DO TRECHO
            </h1>
            <p style="color: #FFCC00 !important; font-size: 1.1rem !important; margin-top: 5px !important; text-align: left !important;">
                Quanto de tempo e de dinheiro são consumidos no seu deslocamento diário?
            </p>
        </div>
    """, unsafe_allow_html=True)

with col_logo:
    try:
        # 'width=120' garante que o logo não fique gigante
        st.image("logo.png", width=180) 
    except:
        st.markdown("<div style='height:80px;'></div>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# PROSSIGA COM O SEU CÓDIGO DE LOCALIZAÇÃO ABAIXO
# ------------------------------------------------------------------

# ------------------------------------------------------------------
# ATENÇÃO: ABAIXO COMEÇA O SEU CÓDIGO ORIGINAL. 
# CERTIFIQUE-SE DE QUE AS PRÓXIMAS LINHAS NÃO SEJAM OUTRO TITULO!
# ------------------------------------------------------------------
# 2. BANCO DE DADOS GEOGRÁFICO
municipios_rmsp = [" "] + sorted(["Arujá", "Barueri", "Biritiba-Mirim", "Caieiras", "Cajamar", "Carapicuíba", "Cotia", "Diadema", "Embu das Artes", "Embu-Guaçu", "Ferraz de Vasconcelos", "Francisco Morato", "Franco da Rocha", "Guararema", "Guarulhos", "Itapecerica da Serra", "Itapevi", "Itaquaquecetuba", "Jandira", "Juquitiba", "Mairiporã", "Mauá", "Mogi das Cruzes", "Osasco", "Pirapora do Bom Jesus", "Poá", "Ribeirão Pires", "Rio Grande da Serra", "Salesópolis", "Santa Isabel", "Santana de Parnaíba", "Santo André", "São Bernardo do Campo", "São Caetano do Sul", "São Lourenço da Serra", "São Paulo", "Suzano", "Taboão da Serra", "Vargem Grande Paulista"])
distritos_sp = [" "] + sorted(["Água Rasa", "Alto de Pinheiros", "Anhanguera", "Aricanduva", "Artur Alvim", "Barra Funda", "Bela Vista", "Belém", "Bom Retiro", "Brasilândia", "Butantã", "Cachoeirinha", "Cambuci", "Campo Belo", "Campo Grande", "Campo Limpo", "Cangaíba", "Capão Redondo", "Carrão", "Casa Verde", "Cidade Ademar", "Cidade Dutra", "Cidade Líder", "Cidade Tiradentes", "Consolação", "Cursino", "Ermelino Matarazzo", "Freguesia do Ó", "Grajaú", "Guaianases", "Iguatemi", "Ipiranga", "Itaim Bibi", "Itaim Paulista", "Itaquera", "Jabaquara", "Jaçanã", "Jaguara", "Jaguaré", "Jaraguá", "Jardim Ângela", "Jardim Helena", "Jardim Paulista", "Jardim São Luís", "Lapa", "Liberdade", "Limão", "Mandaqui", "Marsilac", "Moema", "Mooca", "Morumbi", "Parelheiros", "Pari", "Parque do Carmo", "Pedreira", "Penha", "Perdizes", "Perus", "Pinheiros", "Pirituba", "Ponte Rasa", "Raposo Tavares", "República", "Rio Pequeno", "Sacomã", "Santa Cecília", "Santana", "Santo Amaro", "São Domingos", "São Lucas", "São Mateus", "São Miguel", "São Rafael", "Sapopemba", "Saúde", "Sé", "Socorro", "Tatuapé", "Tremembé", "Tucuruvi", "Vila Andrade", "Vila Curuçá", "Vila Formosa", "Vila Guilherme", "Vila Jacuí", "Vila Leopoldina", "Vila Maria", "Vila Mariana", "Vila Matilde", "Vila Medeiros", "Vila Prudente", "Vila Sônia"])

# 1. SETUP E ESTILO (O ESCUDO DEFINITIVO)
st.set_page_config(page_title="Calculadora do Trecho", layout="wide")

st.markdown("""
    <style>
    /* 1. MATA A FAIXA BRANCA E LIMPA O HEADER */
    header, [data-testid="stHeader"], [data-testid="stStatusWidget"] {
        display: none !important;
    }
    
    /* 2. FUNDO PRETO ABSOLUTO */
    .stApp { background-color: #000000 !important; }
    .block-container { padding-top: 1rem !important; margin-top: -20px !important; }

    /* 3. TÍTULO E TEXTOS (ALINHADOS À ESQUERDA PARA HARMONIZAR COM LOGO À DIREITA) */
    h1 { 
        color: #FFCC00 !important; 
        font-family: 'Arial Black', sans-serif !important; 
        text-align: left !important;
        margin-top: 0px !important;
        padding-top: 10px !important;
    }
    .frase-impacto {
        color: #FFCC00 !important;
        text-align: left !important;
        font-size: 1.1rem !important;
        margin-bottom: 30px !important;
    }
    label, p, span { color: #FFCC00 !important; font-weight: bold !important; }

    /* 4. ESTILO DOS CAMPOS (HÍBRIDO) */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border-radius: 4px !important;
    }
    
    .stTextInput input, .stNumberInput input {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-bottom: 2px solid #FFCC00 !important;
        border-radius: 0px !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

   /* 5. BOTÃO GERAR DIAGNÓSTICO - VERSÃO CORRIGIDA */
    .stButton>button { 
        background-color: #FFCC00 !important; 
        color: #000000 !important; 
        font-weight: 900 !important; 
        width: 100%; height: 4em;
        border: 3px solid #000000 !important; /* Borda preta para destacar */
        text-transform: uppercase;
        box-shadow: none !important;
    }
    
    /* ESSA LINHA ABAIXO "DESENCOBRE" O TEXTO */
    .stButton>button div p { 
        color: #000000 !important; 
        font-weight: 900 !important;
        margin-bottom: 0px !important;
    }

    /* ESTILO DA NOTA TÉCNICA (PAPEL BRANCO) */
    .report-box {
        background-color: #FFFFFF !important;
        padding: 30px;
        border: 6px solid #FFCC00;
        border-radius: 12px;
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 6. ENTRADA DE DADOS: PERFIL DO USUÁRIO (RESTAURADO)
st.markdown("### 👤 PERFIL DO USUÁRIO")
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
st.markdown("### 🚌 CUSTOS DIÁRIOS ('TRANSPORTE (IDA/VOLTA) E RENDIMENTOS')")
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
            <p>• 💹 <b>VALOR DA HORA DE TRABALH0:</b> De R$ {v_h_nom:.2f} para <span style="color:#E63946;">R$ {v_h_re:.2f}</span></p>
            <p>• ⏳ <b>TEMPO DE TRABALHO NÃO PAGO:</b> {h_m:.1f}h/mês</p>
            <p>• 💸 <b>VALOR DO CONFISCO (TARIFA + TEMPO NÃO PAGO):</b> R$ {confi:.2f}</p>
            <p>• 💵 <b>SALÁRIO LÍQUIDO (-TRANSPORTE):</b> R$ {sal_liq_transp:.2f}</p>
            <p>• 📉 <b>{label_sobra}:</b> R$ {sobra:.2f}</p>
       # --- BLOCO FINAL RECONSTRUÍDO ---
        # 1. FORMATAMOS OS VALORES ANTES (Evita erros de símbolos no HTML)
        txt_depre = f"{depre:.1f}%"
        txt_v_hr = f"R$ {v_h_re:.2f}"
        txt_v_hn = f"R$ {v_h_nom:.2f}"
        txt_conf = f"R$ {confi:.2f}"
        txt_liq = f"R$ {sal_liq_transp:.2f}"
        txt_sobra = f"R$ {sobra:.2f}"

        # 2. RESULTADOS (USANDO STRINGS SIMPLES PARA NÃO QUEBRAR)
        st.subheader("Resultados do Diagnóstico")
        
        # Criamos a caixa branca usando uma string única e limpa
        html_res = f"<div style='background-color:#FFFFFF; padding:20px; border:5px solid #FFCC00; border-radius:10px; color:#000000;'>"
        html_res += f"<p style='color:#000000;'>&bull; <b>HORA NOMINAL:</b> {txt_v_hn}</p>"
        html_res += f"<p style='color:#000000;'>&bull; <b>HORA REAL:</b> <span style='color:#E63946;'>{txt_v_hr}</span></p>"
        html_res += f"<p style='color:#000000;'>&bull; <b>TRABALHO NÃO PAGO:</b> {h_m:.1f} h/mês</p>"
        html_res += f"<p style='color:#000000;'>&bull; <b>CONFISCO TOTAL:</b> {txt_conf}</p>"
        html_res += f"<p style='color:#000000;'>&bull; <b>{label_sobra}:</b> {txt_sobra}</p>"
        html_res += f"<p style='color:#000000;'>&bull; <b>DEPRECIAÇÃO:</b> <span style='color:#E63946; font-size:1.2rem; font-weight:bold;'>{txt_depre}</span></p>"
        html_res += "</div>"
        
        st.markdown(html_res, unsafe_allow_html=True)

        # 3. NOTA TÉCNICA (CAIXA BRANCA SEPARADA)
        html_nota = "<div style='background-color:#FFFFFF; padding:20px; border-left:10px solid #FFCC00; border:1px solid #DDD; margin-top:20px; color:#000000;'>"
        html_nota += "<b style='color:#000000;'>📝 NOTA TÉCNICA</b><br>"
        html_nota += "<p style='color:#000000; font-size:0.9rem;'>O Confisco soma a tarifa ao valor do tempo de deslocamento. É o trabalho não pago exigido pela reprodução da força de trabalho.</p></div>"
        
        st.markdown(html_nota, unsafe_allow_html=True)

        # 4. BOTÃO DE DOWNLOAD
        st.download_button("BAIXAR DIAGNÓSTICO", f"Confisco: {txt_conf}\nDepreciação: {txt_depre}", file_name="diagnostico.txt")

