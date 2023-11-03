import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

@st.cache_resource
def load_data():
    df = pd.read_csv('data/base_analise_completa.csv')

    mask = df['npu'].str.contains("0000000000000INATIVA|0000000000000EMGERAL")

    df = df.drop(df[mask].index)

    df.to_csv('data/base_analise_completa.csv', index=False)

    df['distribuido'] = pd.to_datetime(df['distribuido'])
    df['baixado'] = pd.to_datetime(df['baixado'])
    return df

# Carregue os dados usando a função de cache
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
    limite_inferior = datetime(ano_inicial, 1, 1)
    limite_superior = datetime.today()
    return df[(df['distribuido'] >= limite_inferior) & (df['distribuido'] <= limite_superior)]

# Crie um DataFrame filtrado com base no ano escolhido usando a função de cache
df_filtered_hist = filter_data(df, ano_inicial)

# Crie um histograma da coluna "distribuido" usando Plotly Express para as datas filtradas
fig = px.histogram(df_filtered_hist, x='distribuido', title=f'Histograma das Datas de Distribuição ({ano_inicial} até Hoje)', nbins=220)
fig.update_xaxes(title_text='Data de Distribuição')
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

quantidade_p_senha = (df['senha'] == True).sum()
sem_processo = (df['tentativa_de_baixar'].notnull()).sum()
sem_processo_1 = len(df[(df['grau'] == 1) & df['tentativa_de_baixar'].notna()])
sem_processo_2 = len(df[(df['grau'] == 2) & df['tentativa_de_baixar'].notna()])
sem_processo_21 = len(df[(df['grau'] == 21) & df['tentativa_de_baixar'].notna()])
quantidade_grau_1 = len(df[df['grau'] == 1]) - sem_processo_1
quantidade_grau_1_com_recurso = df['processo_primeiro_grau_id'].nunique()
quantidade_grau_1_sem_recurso = quantidade_grau_1 - quantidade_grau_1_com_recurso
quantidade_grau_2_com_primeiro = df[(df['grau'] == 2) & df['processo_primeiro_grau_id'].notnull()].shape[0]
quantidade_grau_2_sem_primeiro = len(df[(df['grau'] == 2) & df['processo_primeiro_grau_id'].isna() & df['processo_principal_id'].isna()])
quantidade_grau_2 = len(df[df['grau'] == 2]) - sem_processo_2
quantidade_grau_21 = len(df[df['grau'] == 21]) -sem_processo_21

# Defina a ordem desejada para as categorias
order = ['com senha','Grau 1 sem Recurso', 'Grau 1 com Recurso', 'Grau 2 com primeiro grau ', 'Grau 2 com Subprocesso', 'Grau 2 sem primeiro grau', 'Grau 21']

data_senha = {
    'Sem Processos': ['quantidade de processos com senha', 'processos consultados sem processos grau 1','processos consultados sem processos grau 2','processos consultados sem processos grau 21'],
    'Quantidade': [quantidade_p_senha, sem_processo_1, sem_processo_2, sem_processo_21]
}

data_1 = {
    'Grau 1': ['Grau 1 sem Recurso', 'Grau 1 com Recurso','Total'],
    'Quantidade': [quantidade_grau_1_sem_recurso, quantidade_grau_1_com_recurso, quantidade_grau_1_com_recurso + quantidade_grau_1_sem_recurso]
}

data_2 = {
    'Grau 2': ['Grau 2 com primeiro grau ', 'Grau 2 com Subprocesso', 'Grau 2 sem primeiro grau', 'Turma Recursal', 'Total'],
    'Quantidade': [quantidade_grau_2_com_primeiro, quantidade_grau_1_sem_recurso, quantidade_grau_2_sem_primeiro, quantidade_grau_21, quantidade_grau_2+quantidade_grau_21 ]
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


