st.markdown("### 💰 ENTRADA DE DADOS")
col_resgate = st.columns(3)

with col_resgate[0]:
    # Mudamos o nome da variável e da key para 'resetar' o navegador
    input_sal = st.number_input("SALÁRIO BRUTO (R$)", min_value=0.0, step=100.0, key="chave_reset_01")
    sal = input_sal # Reatribuímos para não quebrar seus cálculos lá embaixo

with col_resgate[1]:
    input_horas = st.number_input("HORAS NO TRECHO", min_value=0.0, step=0.5, key="chave_reset_02")
    h_dia = input_horas

with col_resgate[2]:
    input_dias = st.number_input("DIAS TRABALHADOS", min_value=1, value=22, key="chave_reset_03")
    dias = input_dias

# Custo de vida com nome novo também
input_cv = st.number_input("CUSTO DE VIDA (R$)", min_value=0.0, key="chave_reset_04")
c_vida = input_cv
