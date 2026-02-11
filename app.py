import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Calculadora do Trecho", layout="centered")

# CSS PARA MÁXIMA NITIDEZ E IDENTIDADE VISUAL
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    
    /* ÍCONE DE INTERROGAÇÃO (?) BRANCO E NÍTIDO */
    .stTooltipIcon { 
        filter: invert(1) brightness(5) !important; 
        transform: scale(1.4); 
    }

    .chamada-impacto { 
        background-color: #E63946; color: white; text-align: center; 
        padding: 12px; font-weight: 900; text-transform: uppercase; 
        border: 2px solid #FFCC00; margin-bottom: 20px; 
    }
    .propisito-app { 
        color: #FFCC00 !important; font-family: 'Arial Black', sans-serif; 
        font-size: 1.8rem !important; text-align: center; text-transform: uppercase; 
        margin-bottom: 5px; 
    }
    .secao-titulo { 
        color: #FFCC00 !important; font-size: 1.1rem !important; 
        font-weight: 800; text-transform: uppercase; 
        margin-top: 25px; border-bottom: 2px solid #FFCC00; padding-bottom: 5px; 
    }
    label { color: #FFCC00 !important; font-weight: 700 !important; font-size: 0.9rem !important; }
    
    /* CARDS DE RESULTADO */
    .card-res { background-color: #111; border: 2px solid #FFCC00; padding: 20px 10px; text-align: center; border-radius: 5px; }
    .val-res { color: #FFCC00 !important; font-size: 1.8rem !important; font-weight: 900 !important; }
    .label-card { color: #FFFFFF !important; font-size: 0.7rem !important; font-weight: bold; text-transform: uppercase; }
    
    /* SÍNTESE FINAL */
    .sintese-box { 
        background-color: #111; border-left: 10px solid #E63946; 
        padding: 25px; margin-top: 30px; color: #FFFFFF; 
        font-size: 1.1rem; line-height: 1.6; 
    }
    </style>
    """, unsafe_allow_html=True)

# LISTA COMPLETA DE MUNICÍPIOS E DISTRITOS
lista_geo = sorted([
    "São Paulo (Centro)", "Água Rasa", "Alto de Pinheiros", "Anhanguera", "Aricanduva", "Artur Alvim", "Barra Funda", "Bela Vista", "Belém", "Bom Retiro", "Brasilândia", "Butantã", "Cachoeirinha", "Cambuci", "Campo Belo", "Campo Grande", "Campo Limpo", "Cangaíba", "Capão Redondo", "Carrão", "Casa Verde", "Cidade Ademar", "Cidade Dutra", "Cidade Líder", "Cidade Tiradentes", "Consolação", "Ermelino Matarazzo", "Freguesia do Ó", "Grajaú", "Guaianases", "Ipiranga", "Itaim Bibi", "Itaim Paulista", "Itaquera", "Jabaquara", "Jaçanã", "Jaguara", "Jaguaré", "Jaraguá", "Jardim Ângela", "Jardim Helena", "Jardim Paulista", "Lapa", "Liberdade", "Limão", "Mandaqui", "Marsilac", "Moema", "Mooca", "Morumbi", "Parelheiros", "Pari", "Parque do Carmo", "Pedreira", "Penha", "Perdizes", "Perus", "Pinheiros", "Pirituba", "Ponte Rasa", "Raposo Tavares", "República", "Rio Pequeno", "Sacomã", "Santa Cecília", "Santana", "Santo Amaro", "São Domingos", "São Lucas", "São Mateus", "São Miguel", "São Rafael", "Sapopemba", "Saúde", "Sé", "Socorro", "Tatuapé", "Tremembé", "Tucuruvi", "Vila Andrade", "Vila Curuçá", "Vila Formosa", "Vila Guilherme", "Vila Jacuí", "Vila Leopoldina", "Vila Maria", "Vila Mariana", "Vila Matilde", "Vila Medeiros", "Vila Prudente", "Vila Sônia",
    "Arujá", "Barueri", "Biritiba-Mirim", "Caieiras", "Cajamar", "Carapicuíba", "Cotia", "Diadema", "Embu das Artes", "Embu-Guaçu", "Ferraz de Vasconcelos", "Francisco Morato", "Franco da Rocha", "Guararema", "Guarulhos", "Itapecerica da Serra", "Itapevi", "Itaquaquecetuba", "Jandira", "Juquitiba", "Mairiporã", "Mauá", "Mogi das Cruzes", "Osasco", "Pirapora do Bom Jesus", "Poá", "Ribeirão Pires", "Rio Grande da Serra", "Salesópolis", "Santa Isabel", "Santana de Parnaíba", "Santo André", "São Bernardo do Campo", "São Caetano do Sul", "São Lourenço da Serra", "Suzano", "Taboão da Serra", "Vargem Grande Paulista"
])

st.markdown('<div class="chamada-impacto">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="propisito-app">QTO DO SEU SALÁRIO FICA NO TRANSPORTE?</div>', unsafe_allow_html=True)

with st.form("main_calc"):
    moradia = st.selectbox("🏠 ONDE VOCÊ MORA?", lista_geo)
    trabalho = st.selectbox("💼 ONDE VOCÊ TRABALHA?", lista_geo)
    
    c1, c2 = st.columns(2)
    with c1:
        sal = st.number_input("💵 SALÁRIO BRUTO (R$):", min_value=0.0, step=100.0)
    with c2:
        vida = st.number_input("🏠 CUSTO VIDA:", min_value=0.0, 
                               help="Preenchimento Opcional: Moradia, alimentação e contas fixas para apurar o rendimento residual após as despesas básicas.")
    
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
    
    # CÁLCULO TÉCNICO: Transporte e Tempo impactam o VALOR DA HORA
    v_hora_real = (sal - custo_t) / (h_paga + h_total)
    perda = (1 - (v_hora_real / (sal/h_paga))) * 100
    
    # SOBRA FINANCEIRA inclui o custo de vida
    sobra_final = sal - custo_t - vida

    r1, r2, r3 = st.columns(3)
    with r1: st.markdown(f'<div class="card-res"><div class="label-card">VALOR REAL PELA<br>HORA DE TRABALHO PAGA</div><div class="val-res">R$ {max(0, v_hora_real):.2f}</div></div>', unsafe_allow_html=True)
    with r2: st.markdown(f'<div class="card-res"><div class="label-card">SALÁRIO REAL<br>CONFISCADO</div><div class="val-res">{max(0, perda):.1f}%</div></div>', unsafe_allow_html=True)
    with r3: st.markdown(f'<div class="card-res"><div class="label-card">TRABALHO NÃO PAGO<br>(HORAS/MÊS)</div><div class="val-res">{h_total:.0f}H</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="secao-titulo">📊 ANÁLISE DA EXPROPRIAÇÃO DO TEMPO</div>', unsafe_allow_html=True)
    fig = go.Figure(data=[go.Pie(labels=['Tempo Remunerado', 'Tempo de Trajeto'], values=[h_paga, h_total], hole=.4, marker_colors=['#FFCC00', '#E63946'], textinfo='percent+label')])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', height=500, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # TEXTO PARA DESLOCAMENTO INTERNO OU EXTERNO
    local_txt = f"por dentro de <b>{moradia}</b>" if moradia == trabalho else f"entre <b>{moradia}</b> e <b>{trabalho}</b>"
    
    # SÍNTESE DINÂMICA
    sintese_vida = f"<br><br><b>RENDIMENTO RESIDUAL:</b> Após o custo de vida (R$ {vida:,.2f}), restam apenas <span style='color:#FFCC00'>R$ {max(0, sobra_final):.2f}</span> mensais para outras necessidades." if vida > 0 else ""

    st.markdown(f"""
        <div class="sintese-box">
            <b>SÍNTESE DA EXPROPRIAÇÃO:</b><br>
            Ao se deslocar {local_txt}, você dedica <span style="color:#FFCC00">{h_total:.0f} horas</span> mensais de trabalho não remunerado ao sistema de mobilidade. 
            O custo do transporte consome R$ {custo_t:,.2f} do seu rendimento. 
            Na prática, seu <b>valor real pela hora de trabalho paga</b> é de <b>R$ {max(0, v_hora_real):.2f}</b>.{sintese_vida}
        </div>
    """, unsafe_allow_html=True)
