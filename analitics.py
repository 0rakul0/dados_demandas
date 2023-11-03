import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

@st.cache_resource
def load_data():
    df = pd.read_csv('data/histograma_valores.csv')
    return df

df = load_data()

st.title("Análise de Demandas Repetitivas ao Longo do Tempo")

st.text(f'As demandas repetivas tem atualmente cerca de {df.shape[0]} observações')

st.header('Introdução:')

st.write("Nesta análise, mergulharemos nas demandas repetitivas em um conjunto de dados que abrange um extenso período de tempo, desde 1950 até os dias atuais. O fenômeno das demandas repetitivas é comum em muitos contextos, e compreender como essas demandas se manifestam ao longo das décadas pode proporcionar insights valiosos sobre tendências e padrões.")

st.write("Nossa análise começa com a seleção de um ano inicial. O controle deslizante permitirá que você escolha o ponto de partida para nossa jornada no tempo, personalizando sua seleção de acordo com seus interesses ou objetivos.")

st.write("Em seguida, apresentaremos um histograma das datas de demandas repetitivas com base no ano inicial escolhido. O histograma revelará como a frequência de demandas repetitivas tem evoluído ao longo do tempo, destacando os momentos de pico e os períodos de menor atividade.")

st.write("Ao explorar esses padrões, esperamos fornecer uma compreensão mais profunda das demandas repetitivas em seu conjunto de dados, o que pode ser essencial para a otimização de recursos, o planejamento de capacidade e a tomada de decisões informadas. Vamos iniciar nossa análise!")

# Defina o valor inicial do controle deslizante
ano_inicial = st.slider('Selecione o ano inicial', 1950, datetime.today().year, 1950)

@st.cache_resource
def filter_data(df, ano_inicial):
    limite_inferior = ano_inicial
    limite_superior = datetime.today().year
    return df[(df['Ano'] >= limite_inferior) & (df['Ano'] <= limite_superior)]

df_filtered_hist = filter_data(df, ano_inicial)

# Crie um histograma da coluna "Ano" usando Plotly Express para as datas filtradas
fig = px.bar(df_filtered_hist, x='Ano', y='Quantidade', title=f'Histograma das Datas de Distribuição ({ano_inicial} até Hoje)')
fig.update_xaxes(title_text='Ano')
fig.update_yaxes(title_text='Frequência')
st.plotly_chart(fig)


st.markdown(
    """
## objetivo da analise

1. **Preparar tabelas com contagens de processo e recursos**: Criar tabelas que incluam contagens de processos e recursos. Isso pode exigir a extração de dados de algum sistema ou banco de dados.

2. **Verificar informações do trânsito em julgado de processos de grau 2 sem grau 1**: Você precisa verificar se há informações sobre o trânsito em julgado de processos de grau 2 que não possuem grau 1. Isso provavelmente envolve a análise de tabelas de movimentos e documentos relacionados.

3. **Avaliar diferenças entre tribunais estaduais**: Após coletar informações sobre os Núcleos de Gerenciamento de Precedentes, você deve avaliar se existem diferenças significativas entre os tribunais estaduais. Isso ajudará a entender se os resultados obtidos no TJSP podem ser generalizados para outros tribunais.

4. **Pesquisar movimentos de levantamento ou suspensão do sobrestamento**: Você deve pesquisar movimentos nos processos que indiquem o levantamento ou suspensão do sobrestamento após o julgamento do STF.
"""
)

st.write('**Preparando as tabelas com contagens de processo e recursos**')

@st.cache_resource
def indicadores_qte():
    df_qte = pd.read_csv('data/indicadores.csv')
    return df_qte

df_qte = indicadores_qte()

quantidade_p_senha = df_qte[df_qte['Indicador'] == 'Quantidade com senha']['Valor'].values[0]
sem_processo = df_qte[df_qte['Indicador'] == 'Quantidade sem processo']['Valor'].values[0]
sem_processo_1 = df_qte[df_qte['Indicador'] == 'Quantidade sem processo (Grau 1)']['Valor'].values[0]
sem_processo_2 = df_qte[df_qte['Indicador'] == 'Quantidade sem processo (Grau 2)']['Valor'].values[0]
sem_processo_21 = df_qte[df_qte['Indicador'] == 'Quantidade sem processo (Grau 21)']['Valor'].values[0]
quantidade_grau_1 = df_qte[df_qte['Indicador'] == 'Quantidade Grau 1']['Valor'].values[0]
quantidade_grau_1_com_recurso = df_qte[df_qte['Indicador'] == 'Quantidade Grau 1 com recurso']['Valor'].values[0]
quantidade_grau_1_sem_recurso = df_qte[df_qte['Indicador'] == 'Quantidade Grau 1 sem recurso']['Valor'].values[0]
quantidade_grau_2_com_primeiro = df_qte[df_qte['Indicador'] == 'Quantidade Grau 2 com primeiro grau']['Valor'].values[0]
quantidade_grau_2_sem_primeiro = df_qte[df_qte['Indicador'] == 'Quantidade Grau 2 sem primeiro grau']['Valor'].values[0]
quantidade_grau_2 = df_qte[df_qte['Indicador'] == 'Quantidade Grau 2']['Valor'].values[0]
quantidade_grau_21 = df_qte[df_qte['Indicador'] == 'Quantidade Grau 21']['Valor'].values[0]
quantidade_grau_21_com_primeiro = df_qte[df_qte['Indicador'] == 'Quantidade Grau 21 com primeiro grau']['Valor'].values[0]
quantidade_grau_21_sem_primeiro = df_qte[df_qte['Indicador'] == 'Quantidade Grau 21 sem primeiro grau']['Valor'].values[0]

data_senha = {
    'Sem Processos': ['quantidade de processos com senha', 'processos consultados sem processos grau 1','processos consultados sem processos grau 2','processos consultados sem processos grau 21'],
    'Quantidade': [quantidade_p_senha, sem_processo_1, sem_processo_2, sem_processo_21]
}

data_1 = {
    'Grau 1': ['Grau 1 sem Recurso', 'Grau 1 com Recurso','Total'],
    'Quantidade': [quantidade_grau_1_sem_recurso, quantidade_grau_1_com_recurso, quantidade_grau_1_com_recurso + quantidade_grau_1_sem_recurso]
}

data_2 = {
    'Grau 2': ['Grau 2 com primeiro grau ', 'Grau 2 com Subprocesso', 'Grau 2 sem primeiro grau','Grau 21 com primeiro grau','Grau 21 sem primeiro grau', 'Turma Recursal', 'Total'],
    'Quantidade': [quantidade_grau_2_com_primeiro, quantidade_grau_1_sem_recurso, quantidade_grau_2_sem_primeiro,quantidade_grau_21_com_primeiro,quantidade_grau_21_sem_primeiro, quantidade_grau_21, quantidade_grau_2+quantidade_grau_21 ]
}

data_geral = {
    'Geral':['primeiro grau','recurso','sem processo'],
    'Quantidade':[quantidade_grau_1, quantidade_grau_2+quantidade_grau_21, sem_processo]
}

df_senha = pd.DataFrame(data_senha)
df_cat_1 = pd.DataFrame(data_1)
df_cat_2 = pd.DataFrame(data_2)
df_info_pie = pd.DataFrame(data_geral)


st.table(df_senha)
st.table(df_cat_1)
st.table(df_cat_2)
st.table(df_info_pie)

fig_qte_grau = px.pie(df_info_pie, names='Geral', values='Quantidade', title='Distribuição dos processos por Grau',
             labels={'Geral': 'Geral', 'Quantidade': 'Quantidade'})

st.plotly_chart(fig_qte_grau)


