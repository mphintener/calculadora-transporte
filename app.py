import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Calculadora do Trecho", layout="centered")

# ESTILO CSS PARA MÁXIMA NITIDEZ E FUNCIONALIDADE DO BALÃO
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    
    /* TÍTULOS PRINCIPAIS */
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
        font-size: 0.9rem !important; 
        margin-bottom: 30px; 
    }

    /* CHAMADA DE IMPACTO */
    .chamada-impacto {
        background-color: #E63946;
        color: white;
        text-align: center;
        padding: 10px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 20px;
        border: 2px solid #FFCC00;
    }

    /* TÍTULOS DE SEÇÃO (CORRIGINDO NITIDEZ E TAMANHO) */
    .secao-titulo {
        color: #FFCC00 !important;
        font-size: 1rem !important;
        font-weight: 800;
        text-transform: uppercase;
        margin-top: 25px;
        margin-bottom: 15px;
        border-bottom: 1px solid #FFCC00;
        padding-bottom: 5px;
    }

    /* LABELS E INPUTS */
    label { color: #FFCC00 !important; font-weight: 700 !important; font-size: 0.85rem !important; }
    
    div[data-baseweb="select"], div[data-baseweb="input"], .stSlider { 
        border: 1px solid #FFCC00 !important; 
        background-color: #111 !important; 
    }

    /* CARDS DE RESULTADO */
    .card-res { background-color: #111; border: 2px solid #FFCC00; padding: 20px 10px; text-align: center; border-radius: 5px; }
    .val-res { color: #FFCC00 !important; font-size: 1.8rem !important; font-weight: 900 !important; }
    .label-card { color: #FFFFFF !important; font-size: 0.7rem !important; font-weight: bold; }
    
    /* SÍNTESE FINAL */
    .sintese-box {
        background-color: #111;
        border-left: 8px solid #FFCC00;
        padding: 20px;
        margin-top: 30px;
        color: #FFFFFF;
        font-size: 1rem;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. CABEÇALHO
st.markdown('<div class="chamada-impacto">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="propisito-app">QTO DO SEU SALÁRIO FICA NO TRANSPORTE?</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-metodo">CÁLCULO DE RENDIMENTO REAL E EXPROPRIAÇÃO DE TEMPO</div>', unsafe_allow_html=True)

# 2. FORMULÁRIO
with st.form("main_calc"):
    lista_geo = sorted(["São Paulo (Capital)", "Guarulhos", "São Bernardo", "Santo André", "Osasco", "Mogi das Cruzes", "Mauá", "Diadema", "Carapicuíba", "Itaquaquecetuba", "Barueri", "Taboão da Serra", "Suzano", "Cotia", "Itapevi", "Franco da Rocha", "Caieiras", "Aricanduva", "Butantã", "Lapa", "Itaquera", "Capão Redondo", "Grajaú"])
    
    moradia = st.selectbox("🏠 ONDE VOCÊ MORA?", lista_geo)
    trabalho = st.selectbox("💼 ONDE VOCÊ TRABALHA?", lista_geo)
    
    c1, c2 = st.columns(2)
    with c1: sal = st.number_input("💵 SALÁRIO BRUTO (R$):", min_value=0.0, step=100.0)
    # BALÃO DE INFORMAÇÃO (HELP) RE-INSERIDO
    with c2: vida = st.number_input("🏠 CUSTO VIDA:", min_value=0.0, help="Preenchimento opcional. Inclua gastos fixos como aluguel, luz e alimentação básica.")
    
    st.markdown('<div class="secao-titulo">🚌 GASTOS DIÁRIOS (IDA+VOLTA)</div>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1: p_pub = st.number_input("🚆 PÚBLICO (R$)", min_value=0.0)
    with g2: p_app = st.number_input("📱 APP (R$)", min_value=0.0)
    with g3: p_car = st.number_input("🚗 CARRO (R$)", min_value=0.0)
    
    st.markdown('<div class="secao-titulo">⏱️ TEMPO DE DESLOCAMENTO</div>', unsafe_allow_html=True)
    h_trecho = st.slider("TOTAL DE HORAS NO TRECHO POR DIA (IDA+VOLTA):", 0.5, 12.0, 2.0, step=0.5)
    
    btn = st.form_submit_button("EFETUAR CÁLCULO DE IMPACTO")

# 3. RESULTADOS E SÍNTESE
if btn and sal > 0:
    dias, h_paga = 22, 176
    custo_t = (p_pub + p_app + p_car) * dias
    h_total = h_trecho * dias
    sobra = sal - custo_t - vida
    v_hora_real = sobra / (h_paga + h_total)
    perda = (1 - (v_hora_real / (sal/h_paga))) * 100

    r1, r2, r3 = st.columns(3)
    with r1: st.markdown(f'<div class="card-res"><div class="label-card">VALOR REAL PAGO PELA<br>HORA TRABALHADA</div><div class="val-res">R$ {max(0, v_hora_real):.2f}</div></div>', unsafe_allow_html=True)
    with r2: st.markdown(f'<div class="card-res"><div class="label-card">SALÁRIO REAL<br>CONFISCADO</div><div class="val-res">{max(0, perda):.1f}%</div></div>', unsafe_allow_html=True)
    with r3: st.markdown(f'<div class="card-res"><div class="label-card">TRABALHO NÃO PAGO<br>(HORAS/MÊS)</div><div class="val-res">{h_total:.0f}H</div></div>', unsafe_allow_html=True)

    # GRÁFICO
    st.write("### 📊 DISTRIBUIÇÃO DO TEMPO DE VIDA MENSAL")
    fig = go.Figure(data=[go.Pie(labels=['Tempo Remunerado', 'Tempo Expropriado'], values=[h_paga, h_total], hole=.5, marker_colors=['#FFCC00', '#E63946'])])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', showlegend=False, height=300)
    st.plotly_chart(fig, use_container_width=True)

    

    # SÍNTESE FINAL (INFORMAÇÃO EXPLICATIVA)
    st.markdown(f"""
        <div class="sintese-box">
            <b>SÍNTESE DO IMPACTO:</b><br>
            Ao se deslocar entre {moradia} e {trabalho}, você dedica <span style="color:#FFCC00">{h_total:.0f} horas</span> do seu mês ao trajeto. 
            Este tempo, somado ao custo financeiro do transporte, reduz o valor da sua hora trabalhada para 
            <span style="color:#FFCC00">R$ {max(0, v_hora_real):.2f}</span>. 
            Isso revela que o sistema de mobilidade confisca uma parcela significativa da sua força de trabalho antes mesmo dela ser exercida.
        </div>
    """, unsafe_allow_html=True)
