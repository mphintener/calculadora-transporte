import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. ESTILO TERMINAL URBANO (PRETO, AMARELO 99, VERMELHO SPTRANS)
st.set_page_config(page_title="Calculadora do Trecho", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    
    .propisito-app {
        color: #FFCC00 !important;
        font-family: 'Arial Black', sans-serif;
        font-size: 1.8rem !important;
        text-align: center;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    .sub-metodo {
        color: #FFFFFF !important;
        text-align: center;
        font-size: 0.85rem !important;
        margin-bottom: 25px;
        font-weight: bold;
    }

    /* LABELS AMARELO 99 */
    label, p, h3 { 
        color: #FFCC00 !important; 
        font-weight: 800 !important; 
        text-transform: uppercase !important;
    }

    /* BORDAS E INPUTS */
    div[data-baseweb="select"], div[data-baseweb="input"] {
        border: 2px solid #FFCC00 !important;
        border-radius: 4px;
    }

    /* BOTÃO SPTRANS */
    div.stButton > button {
        background-color: #E63946 !important;
        color: #FFFFFF !important;
        font-weight: 900 !important;
        width: 100% !important;
        height: 4rem !important;
        font-size: 1.4rem !important;
        border: 2px solid #FFFFFF !important;
        text-transform: uppercase;
    }

    /* CARDS DE RESULTADO */
    .card-res {
        background-color: #111;
        border: 3px solid #FFCC00;
        padding: 20px 10px;
        text-align: center;
        border-radius: 10px;
        min-height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .val-res { color: #FFCC00 !important; font-size: 1.8rem !important; font-weight: 900 !important; }
    .label-card { color: #FFFFFF !important; font-size: 0.7rem !important; font-weight: bold; margin-bottom: 10px; }
    
    /* ALERTA SALÁRIO LIVRE */
    .alerta-final {
        background-color: #111;
        border-left: 10px solid #E63946;
        padding: 25px;
        margin-top: 30px;
        color: #FFFFFF;
        font-family: monospace;
    }
    .destaque { color: #FFCC00; font-weight: bold; font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

# 2. GEOGRAFIA
lista_geo = sorted(["São Paulo (Capital)", "Guarulhos", "São Bernardo", "Santo André", "Osasco", "Mogi das Cruzes", "Mauá", "Diadema", "Carapicuíba", "Itaquaquecetuba", "Barueri", "Taboão da Serra", "Suzano", "Cotia", "Itapevi", "Ferraz de Vasconcelos", "Franco da Rocha", "Itapecerica", "Ribeirão Pires", "Santana de Parnaíba", "Cajamar", "Embu das Artes", "Caieiras", "Arujá", "Poá", "Água Rasa", "Alto de Pinheiros", "Aricanduva", "Artur Alvim", "Barra Funda", "Bela Vista", "Belém", "Bom Retiro", "Brasilândia", "Butantã", "Cambuci", "Campo Belo", "Campo Grande", "Campo Limpo", "Capão Redondo", "Carrão", "Casa Verde", "Cidade Ademar", "Cidade Dutra", "Cidade Líder", "Cidade Tiradentes", "Consolação", "Ermelino Matarazzo", "Freguesia do Ó", "Grajaú", "Guaianases", "Ipiranga", "Itaim Bibi", "Itaim Paulista", "Itaquera", "Jabaquara", "Jaçanã", "Jaguara", "Jaguaré", "Jaraguá", "Jardim Ângela", "Lapa", "Liberdade", "Limão", "Moema", "Mooca", "Morumbi", "Parelheiros", "Penha", "Perdizes", "Perus", "Pinheiros", "Pirituba", "Ponte Rasa", "República", "Sacomã", "Santana", "Santo Amaro", "Saúde", "Sé", "Socorro", "Tatuapé", "Tremembé", "Tucuruvi", "Vila Andrade", "Vila Curuçá", "Vila Formosa", "Vila Guilherme", "Vila Mariana", "Vila Matilde", "Vila Medeiros", "Vila Prudente", "Vila Sônia"])

# 3. CONTEÚDO
st.markdown('<div class="propisito-app">QTO DO SEU SALÁRIO FICA NO TRANSPORTE?</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-metodo">CÁLCULO DE RENDIMENTO REAL E EXPROPRIAÇÃO DE TEMPO</div>', unsafe_allow_html=True)

with st.form("calc_form"):
    origem = st.selectbox("🏠 MORO EM:", lista_geo)
    destino = st.selectbox("💼 TRABALHO EM:", lista_geo)
    
    c1, c2 = st.columns(2)
    with c1: sal_bruto = st.number_input("💵 SALÁRIO BRUTO (R$):", min_value=0.0, step=100.0)
    # BALÃO DE INFO (HELP) CONFIGURADO
    with c2: c_vida = st.number_input("🏠 CUSTO VIDA:", min_value=0.0, help="OPCIONAL: Inclua gastos com Aluguel, Alimentação e Contas para calcular o que sobra de fato.")
    
    st.write("### 🚌 GASTOS DIÁRIOS (IDA-VOLTA)")
    g1, g2, g3 = st.columns(3)
    with g1: p_pub = st.number_input("🚆 PÚBLICO (R$)", min_value=0.0)
    with g2: p_app = st.number_input("📱 APP (R$)", min_value=0.0)
    with g3: p_car = st.number_input("🚗 CARRO (R$)", min_value=0.0)
    
    st.write("---")
    h_trecho = st.slider("⏱️ HORAS NO TRECHO / DIA (TOTAL):", 0.5, 12.0, 2.0, step=0.5)
    
    btn = st.form_submit_button("CALCULAR IMPACTO REAL")

# 4. RESULTADOS (CEREJA DO BOLO)
if btn and sal_bruto > 0:
    dias, h_paga_mes = 22, 176
    custo_transp = (p_pub + p_app + p_car) * dias
    h_total_trecho = h_trecho * dias
    sobra = sal_bruto - custo_transp - c_vida
    # Termo solicitado: VALOR REAL PAGO PELA HORA TRABALHADA
    v_hora_real = sobra / (h_paga_mes + h_total_trecho)
    perda_pct = (1 - (v_hora_real / (sal_bruto/h_paga_mes))) * 100

    r1, r2, r3 = st.columns(3)
    with r1: st.markdown(f'<div class="card-res"><div class="label-card">VALOR REAL PAGO PELA<br>HORA TRABALHADA</div><div class="val-res">R$ {max(0, v_hora_real):.2f}</div></div>', unsafe_allow_html=True)
    with r2: st.markdown(f'<div class="card-res"><div class="label-card">SALÁRIO REAL<br>CONFISCADO</div><div class="val-res">{max(0, perda_pct):.1f}%</div></div>', unsafe_allow_html=True)
    with r3: st.markdown(f'<div class="card-res"><div class="label-card">TRABALHO GRÁTIS<br>(HORAS/MÊS)</div><div class="val-res">{h_total_trecho:.0f}H</div></div>', unsafe_allow_html=True)

    

    st.write("### 📊 DIVISÃO DO SEU TEMPO MENSAL")
    fig = go.Figure(data=[go.Pie(
        labels=['Tempo Pago', 'Tempo Perdido'],
        values=[h_paga_mes, h_total_trecho],
        hole=.5, marker_colors=['#FFCC00', '#E63946'],
        textinfo='label+percent', textfont=dict(color="white", size=14)
    )])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', showlegend=False, height=350)
    st.plotly_chart(fig, width='stretch')

    st.markdown(f"""
        <div class="alerta-final">
            🚨 <b>SALÁRIO LIVRE:</b><br>
            DO SEU BRUTO DE R$ {sal_bruto:,.2f}, RESTAM <span class="destaque">R$ {max(0, sobra):.2f}</span><br>
            APÓS DESCONTAR TRANSPORTE (R$ {custo_transp:,.2f}) E VIDA (R$ {c_vida:,.2f}).
        </div>
    """, unsafe_allow_html=True)

    st.info(f"**SÍNTESE:** O deslocamento entre {origem} e {destino} confisca seu tempo e renda. Este cálculo demonstra a desvalorização real da sua força de trabalho.")
