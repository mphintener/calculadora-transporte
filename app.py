import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Calculadora do Trecho", layout="centered")

# CSS REVISADO PARA GARANTIR NITIDEZ E FUNCIONAMENTO DO BALÃO (HELP)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    
    .chamada-impacto {
        background-color: #E63946; color: white; text-align: center;
        padding: 8px; font-weight: 900; text-transform: uppercase;
        letter-spacing: 1px; margin-bottom: 15px; border: 2px solid #FFCC00;
        font-size: 0.9rem;
    }

    .propisito-app { 
        color: #FFCC00 !important; font-family: 'Arial Black', sans-serif; 
        font-size: 1.6rem !important; text-align: center; text-transform: uppercase;
        margin-bottom: 5px; line-height: 1.1;
    }
    
    .sub-metodo { 
        color: #FFFFFF !important; text-align: center; 
        font-size: 0.8rem !important; margin-bottom: 25px; 
    }

    /* TÍTULOS DE SEÇÃO NÍTIDOS */
    .secao-titulo {
        color: #FFCC00 !important; font-size: 1rem !important;
        font-weight: 800; text-transform: uppercase;
        margin-top: 25px; margin-bottom: 15px;
        border-bottom: 2px solid #FFCC00; padding-bottom: 5px;
    }

    /* LABELS AJUSTADAS PARA O BALÃO APARECER */
    label { 
        color: #FFCC00 !important; 
        font-weight: 700 !important; 
        font-size: 0.85rem !important;
        display: inline-flex !important;
        align-items: center !important;
    }
    
    .card-res { background-color: #111; border: 2px solid #FFCC00; padding: 15px 5px; text-align: center; border-radius: 5px; height: 115px; }
    .val-res { color: #FFCC00 !important; font-size: 1.6rem !important; font-weight: 900 !important; }
    .label-card { color: #FFFFFF !important; font-size: 0.65rem !important; font-weight: bold; text-transform: uppercase; }
    
    .sintese-box {
        background-color: #111; border-left: 8px solid #FFCC00;
        padding: 15px; margin-top: 25px; color: #FFFFFF;
        font-size: 0.95rem; line-height: 1.5; border-radius: 0 5px 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# LISTA COMPLETA
lista_geo = sorted([
    "São Paulo (Capital)", "Guarulhos", "São Bernardo", "Santo André", "Osasco", "Mogi das Cruzes", "Mauá", "Diadema", 
    "Carapicuíba", "Itaquaquecetuba", "Barueri", "Taboão da Serra", "Suzano", "Cotia", "Itapevi", "Ferraz de Vasconcelos", 
    "Franco da Rocha", "Itapecerica", "Ribeirão Pires", "Santana de Parnaíba", "Cajamar", "Embu das Artes", "Caieiras", 
    "Arujá", "Poá", "Água Rasa", "Alto de Pinheiros", "Aricanduva", "Artur Alvim", "Barra Funda", "Bela Vista", "Belém", 
    "Bom Retiro", "Brasilândia", "Butantã", "Cambuci", "Campo Belo", "Campo Grande", "Campo Limpo", "Capão Redondo", 
    "Carrão", "Casa Verde", "Cidade Ademar", "Cidade Dutra", "Cidade Líder", "Cidade Tiradentes", "Consolação", 
    "Ermelino Matarazzo", "Freguesia do Ó", "Grajaú", "Guaianases", "Ipiranga", "Itaim Bibi", "Itaim Paulista", 
    "Itaquera", "Jabaquara", "Jaçanã", "Jaguara", "Jaguaré", "Jaraguá", "Jardim Ângela", "Lapa", "Liberdade", "Limão", 
    "Moema", "Mooca", "Morumbi", "Parelheiros", "Penha", "Perdizes", "Perus", "Pinheiros", "Pirituba", "Ponte Rasa", 
    "República", "Sacomã", "Santana", "Santo Amaro", "Saúde", "Sé", "Socorro", "Tatuapé", "Tremembé", "Tucuruvi", 
    "Vila Andrade", "Vila Curuçá", "Vila Formosa", "Vila Guilherme", "Vila Mariana", "Vila Matilde", "Vila Medeiros", 
    "Vila Prudente", "Vila Sônia"
])

st.markdown('<div class="chamada-impacto">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="propisito-app">QTO DO SEU SALÁRIO FICA NO TRANSPORTE?</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-metodo">CÁLCULO DE RENDIMENTO REAL E EXPROPRIAÇÃO DE TEMPO</div>', unsafe_allow_html=True)

with st.form("main_calc"):
    moradia = st.selectbox("🏠 ONDE VOCÊ MORA?", lista_geo)
    trabalho = st.selectbox("💼 ONDE VOCÊ TRABALHA?", lista_geo)
    
    col1, col2 = st.columns(2)
    with col1:
        sal = st.number_input("💵 SALÁRIO BRUTO (R$):", min_value=0.0, step=100.0)
    with col2:
        # O PARÂMETRO HELP ABAIXO GERA O BALÃO DE INFORMAÇÃO
        vida = st.number_input("🏠 CUSTO VIDA:", min_value=0.0, help="OPCIONAL: Aluguel, Alimentação e Contas Fixas para calcular a sobra real.")
    
    st.markdown('<div class="secao-titulo">🚌 GASTOS DIÁRIOS (IDA+VOLTA)</div>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1: p_pub = st.number_input("🚆 PÚBLICO (R$)", min_value=0.0)
    with g2: p_app = st.number_input("📱 APP (R$)", min_value=0.0)
    with g3: p_car = st.number_input("🚗 CARRO (R$)", min_value=0.0)
    
    st.markdown('<div class="secao-titulo">⏱️ TEMPO DE DESLOCAMENTO</div>', unsafe_allow_html=True)
    h_trecho = st.slider("TOTAL DE HORAS NO TRECHO POR DIA (IDA+VOLTA):", 0.5, 12.0, 2.0, step=0.5)
    
    btn = st.form_submit_button("EFETUAR CÁLCULO DE IMPACTO")

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

    st.write("---")
    fig = go.Figure(data=[go.Pie(labels=['Tempo Remunerado', 'Tempo Expropriado'], values=[h_paga, h_total], hole=.5, marker_colors=['#FFCC00', '#E63946'])])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', showlegend=False, height=300)
    st.plotly_chart(fig, use_container_width=True)

    

    st.markdown(f"""
        <div class="sintese-box">
            <b>SÍNTESE DO IMPACTO:</b><br>
            Ao se deslocar entre <b>{moradia}</b> e <b>{trabalho}</b>, você dedica <span style="color:#FFCC00">{h_total:.0f} horas</span> mensais apenas ao trajeto. 
            Este tempo, somado ao custo do transporte, reduz o valor da sua hora trabalhada para 
            <span style="color:#FFCC00">R$ {max(0, v_hora_real):.2f}</span>. 
            Isso revela que o sistema de mobilidade confisca uma parcela significativa da sua vida antes mesmo de você chegar ao trabalho.
        </div>
    """, unsafe_allow_html=True)
