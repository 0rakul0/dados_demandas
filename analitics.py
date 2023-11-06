import streamlit as st
import pandas as pd
from datetime import datetime

@st.cache_resource
def load_data():
    df = pd.read_csv('data/histograma_valores.csv')
    return df

df = load_data()

st.title("Análise de Demandas Repetitivas ao Longo do Tempo")


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

st.bar_chart(df_filtered_hist.set_index('Ano'))

st.markdown(
    """
## Objetivo da analise

1. **Preparar tabelas com contagens de processo e recursos**: Criar tabelas que incluam contagens de processos e recursos. Isso pode exigir a extração de dados de algum sistema ou banco de dados.

2. **Verificar informações do trânsito em julgado de processos de grau 2 sem grau 1**: Você precisa verificar se há informações sobre o trânsito em julgado de processos de grau 2 que não possuem grau 1. Isso provavelmente envolve a análise de tabelas de movimentos e documentos relacionados.

3. **Avaliar diferenças entre tribunais estaduais**: Após coletar informações sobre os Núcleos de Gerenciamento de Precedentes, você deve avaliar se existem diferenças significativas entre os tribunais estaduais. Isso ajudará a entender se os resultados obtidos no TJSP podem ser generalizados para outros tribunais.

4. **Pesquisar movimentos de levantamento ou suspensão do sobrestamento**: Você deve pesquisar movimentos nos processos que indiquem o levantamento ou suspensão do sobrestamento após o julgamento do STF.
"""
)


@st.cache_resource
def indicadores_qte():
    df_qte = pd.read_csv('data/indicadores.csv')
    return df_qte


df_indicadores = indicadores_qte()

indicadores = df_indicadores.set_index('Indicador')['Valor'].to_dict()

quantidade_p_senha = indicadores.get('Quantidade com senha', 0)
sem_processo = indicadores.get('Quantidade sem processo', 0)
sem_processo_1 = indicadores.get('Quantidade sem processo (Grau 1)', 0)
sem_processo_2 = indicadores.get('Quantidade sem processo (Grau 2)', 0)
sem_processo_21 = indicadores.get('Quantidade sem processo (Grau 21)', 0)

quantidade_grau_1 = indicadores.get('Quantidade Grau 1', 0)
quantidade_grau_2 = indicadores.get('Quantidade Grau 2', 0)
quantidade_grau_21 = indicadores.get('Quantidade Grau 21', 0)

quantidade_grau_1_com_recurso = indicadores.get('Quantidade Grau 1 com recurso', 0)
quantidade_grau_1_sem_recurso = indicadores.get('Quantidade Grau 1 sem recurso', 0)

quantidade_grau_2_com_primeiro = indicadores.get('Quantidade Grau 2 com primeiro grau', 0)
quantidade_grau_2_sem_primeiro = indicadores.get('Quantidade Grau 2 sem primeiro grau', 0)
quantidade_grau_2_com_recurso = indicadores.get('Quantidade Grau 2 com recurso', 0)
quantidade_grau_2_sem_recurso = indicadores.get('Quantidade Grau 2 sem recurso', 0)
quantidade_grau_21_com_primeiro = indicadores.get('Quantidade Grau 21 com primeiro grau', 0)
quantidade_grau_21_sem_primeiro = indicadores.get('Quantidade Grau 21 sem primeiro grau', 0)
quantidade_grau_21_com_recurso = indicadores.get('Quantidade Grau 21 com recurso', 0)
quantidade_grau_21_sem_recurso = indicadores.get('Quantidade Grau 21 sem recurso', 0)

quantidade_grau_1_0000 = indicadores.get('Quantidade com 0000 (Grau 1)', 0)
quantidade_grau_2_0000 = indicadores.get('Quantidade com 0000 (Grau 2)', 0)
quantidade_grau_21_0000 = indicadores.get('Quantidade com 0000 (Grau 21)', 0)

recurso =quantidade_grau_2 + quantidade_grau_21
sem_extracao = sem_processo + quantidade_p_senha
total = quantidade_grau_1 + quantidade_grau_2 + quantidade_grau_21 + quantidade_p_senha + sem_processo

st.text(f'As demandas repetivas tem atualmente cerca de {total} observações')

data_senha = {
    'Sem Processos': ['quantidade de processos com senha', 'processos consultados sem processos grau 1','processos consultados sem processos grau 2','processos consultados sem processos grau 21', 'Total Sem Processo ou com senha'],
    'Quantidade': [quantidade_p_senha, sem_processo_1, sem_processo_2, sem_processo_21, sem_extracao]
}

data_0000 = {
    'Processos terminados com 0000 por grau':['Quantidade com 0000 (Grau 1)','Quantidade com 0000 (Grau 2)','Quantidade com 0000 (Grau 21)'],
    'Quantidade':[quantidade_grau_1_0000, quantidade_grau_2_0000, quantidade_grau_21_0000]
}

data_1 = {
    'Grau 1': ['Grau 1 sem Recurso', 'Grau 1 com Recurso','Total'],
    'Quantidade': [quantidade_grau_1_sem_recurso, quantidade_grau_1_com_recurso, quantidade_grau_1_com_recurso + quantidade_grau_1_sem_recurso]
}

data_2 = {
    'Recursos': ['Quantidade Grau 2 com primeiro grau','Quantidade Grau 2 sem primeiro grau','Quantidade Grau 2 com recurso','Quantidade Grau 2 sem recurso',
                 'Quantidade Grau 21 com primeiro grau','Quantidade Grau 21 sem primeiro grau','Quantidade Grau 21 com recurso','Quantidade Grau 21 sem recurso'],
    'Quantidade': [quantidade_grau_2_com_primeiro,quantidade_grau_2_sem_primeiro,quantidade_grau_2_com_recurso,quantidade_grau_2_sem_recurso,
                   quantidade_grau_21_com_primeiro,quantidade_grau_21_sem_primeiro,quantidade_grau_21_com_recurso,quantidade_grau_21_sem_recurso]
}

data_geral = {
    'Geral':['Primeiro grau','Recursos','Sem processo e processo com senha'],
    'Quantidade':[quantidade_grau_1, recurso, sem_extracao]
}


df_senha = pd.DataFrame(data_senha)
df_0000 = pd.DataFrame(data_0000)
df_cat_1 = pd.DataFrame(data_1)
df_cat_2 = pd.DataFrame(data_2)
df_info_pie = pd.DataFrame(data_geral)


st.subheader('Primeiro Grau (Processos Sobrestados)')
st.markdown("""
O termo "Primeiro Grau" nesta análise refere-se a processos judiciais que estão temporariamente suspensos ou sobrestados por uma razão específica.
Processos sobrestados podem estar aguardando a conclusão de ações relacionadas (STF), como processos em outros tribunais ou instâncias.
A suspensão temporária é muitas vezes uma prática comum para permitir que questões específicas sejam resolvidas ou desenvolvam-se antes que o processo continue.
A análise desses casos pode fornecer insights sobre a complexidade do sistema judicial e a gestão de processos em várias fases.
""")

Proporcao_1 = round((quantidade_grau_1 / total) * 100)
st.write(f'Em nosso estudo cerca de a proporção da categoria "Primeiro Grau" em relação ao total é {Proporcao_1}%.')
st.write('Esses números se referem a processos no grau 1, categorizados como "com recurso" ou "sem recurso". O total representa o número total de processos no grau 1.')
st.table(df_cat_1)

Proporcao_2 = round((recurso / total) * 100)
st.write(f'A proporção de recursos de grau 2 referente ao "Primeiro Grau" é de {Proporcao_2}%.')
st.write('Esses números representam processos nos graus 2 e 21, classificados com base na presença ou ausência de "primeiro grau" e na presença ou ausência de "recurso".')
st.table(df_cat_2)

Proporcao_3 = round((sem_extracao/total) * 100)
st.write(f'A proporção de processos que não foi possivel extrai ou protegido de grau 2 referente ao "Primeiro Grau" é de {Proporcao_3}%.')
st.write('Esses números indicam a quantidade de processos que estão protegidos por senhas e a quantidade de processos sem informações disponíveis nos graus 1 e 2.')
st.table(df_senha)

st.write('Esses números indicam a quantidade de processos que tem o final de seu npu "0000" em diferentes graus. Exemplo: xxxxxxx-dd.yyyy.8.26.0000')
st.table(df_0000)

st.write('Esses números fornecem uma visão geral dos processos no primeiro grau, processos de recurso e a quantidade de processos sem informações disponíveis ou protegidos por senha.')
st.table(df_info_pie)
st.write(f'Assim temos as seguintes proporções {Proporcao_1}% para o primeiro grau {Proporcao_2}% de recursos e {Proporcao_3}% para processo que estavam ou protegidos ou com algum tipo de bloqueio')
st.bar_chart(df_info_pie.set_index('Geral'))


st.header('Analise dos Juizes por classe classes')

st.write('O ranking foi montado usando o nome do Juiz como referencia')

@st.cache_resource
def load_classe_juiz():
    result_df_classe = pd.read_csv('data/ranking_classe_juizes.csv')
    return result_df_classe
result_df_classe = load_classe_juiz()

st.write('Como podemos observar o ranking varia muito com o passar dos anos assim como a quantidade de classes processuais')

selected_year_classe = st.slider('Selecione o ano', min_value=1950, max_value=2023)
filtered_df_classe = result_df_classe[result_df_classe['ano'] == selected_year_classe]
processos_por_classe_juiz= filtered_df_classe.groupby(['nome_juiz','nome_classe']).size().reset_index(name='quantidade_processos')
processos_por_classe_juiz = processos_por_classe_juiz.sort_values(by='quantidade_processos', ascending=False)
top_10_classe = processos_por_classe_juiz.head(10)
st.table(top_10_classe)
st.bar_chart(top_10_classe.set_index('nome_juiz')['quantidade_processos'])


processos_por_juiz = result_df_classe.groupby('nome_juiz')['p_id'].count()
processos_por_juiz = processos_por_juiz.reset_index()
processos_por_juiz = processos_por_juiz.rename(columns={'p_id': 'quantidade_processos'})
processos_por_juiz = processos_por_juiz.sort_values(by='quantidade_processos', ascending=False)
st.write('Quantidade de processos por juiz')
processos_por_juiz = processos_por_juiz.head(10)
st.table(processos_por_juiz)

processos_por_classe = result_df_classe.groupby('nome_classe')['p_id'].count()
processos_por_classe = processos_por_classe.reset_index()
processos_por_classe = processos_por_classe.rename(columns={'p_id': 'quantidade_processos'})
processos_por_classe = processos_por_classe.sort_values(by='quantidade_processos', ascending=False)
st.write('Quantidade de processos por classe')
processos_por_classe = processos_por_classe.head(10)
st.table(processos_por_classe)

