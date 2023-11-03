import pandas as pd

def load_data():
    df = pd.read_csv('data/base_analise_completa.csv')

    mask = df['npu'].str.contains("0000000000000INATIVA|0000000000000EMGERAL")

    df = df.drop(df[mask].index)

    df.to_csv('data/base_analise_completa.csv', index=False)

    df['distribuido'] = pd.to_datetime(df['distribuido'])
    df['baixado'] = pd.to_datetime(df['baixado'])

    anos = range(1950, 2024)  # Defina o intervalo de anos
    histogram_values = []

    for ano in anos:
        df_filtered_hist = df[df['distribuido'].dt.year == ano]
        histogram_values.append(len(df_filtered_hist))

    histogram_df = pd.DataFrame({'Ano': anos, 'Quantidade': histogram_values})

    # Salve o DataFrame em um arquivo CSV
    histogram_df.to_csv('data/histograma_valores.csv', index=False)

    return df

df = load_data()
quantidade_p_senha = df.query("senha == True").shape[0]
sem_processo = df.query("tentativa_de_baixar.notnull()").shape[0]
sem_processo_1 = df.query("grau == 1 and tentativa_de_baixar.notnull()").shape[0]
sem_processo_2 = df.query("grau == 2 and tentativa_de_baixar.notnull()").shape[0]
sem_processo_21 = df.query("grau == 21 and tentativa_de_baixar.notnull()").shape[0]
quantidade_grau_1 = df.query("grau == 1 and tentativa_de_baixar.isna()").shape[0]
quantidade_grau_2 = df.query("grau == 2 and tentativa_de_baixar.isna()").shape[0]
quantidade_grau_21 = df.query("grau == 21 and tentativa_de_baixar.isna()").shape[0]

quantidade_grau_1_com_recurso = df['processo_primeiro_grau_id'].nunique()
quantidade_grau_1_sem_recurso = quantidade_grau_1 - quantidade_grau_1_com_recurso

quantidade_grau_2_com_primeiro = df.query("grau == 2 and tentativa_de_baixar.isna() and processo_primeiro_grau_id.notnull()").shape[0]
quantidade_grau_2_sem_primeiro = df.query("grau == 2 and tentativa_de_baixar.isna() and processo_primeiro_grau_id.isna()").shape[0]
quantidade_grau_2_com_recurso = df.query("grau == 2 and tentativa_de_baixar.isna() and observacao.notnull()").shape[0]
quantidade_grau_2_sem_recurso = df.query("grau == 2 and tentativa_de_baixar.isna() and observacao.isna()").shape[0]

quantidade_grau_21_com_primeiro = df.query("grau == 21 and tentativa_de_baixar.isna() and processo_primeiro_grau_id.notnull()").shape[0]
quantidade_grau_21_sem_primeiro = df.query("grau == 21 and tentativa_de_baixar.isna() and processo_primeiro_grau_id.isna()").shape[0]
quantidade_grau_21_com_recurso = df.query("grau == 21 and tentativa_de_baixar.isna() and observacao.notnull()").shape[0]
quantidade_grau_21_sem_recurso = df.query("grau == 21 and tentativa_de_baixar.isna() and observacao.isna()").shape[0]

dados_filtrados = df[df['npu'].str.endswith('8260000')]
quantidade_processos_com_0000 = dados_filtrados['grau'].value_counts().reset_index()
quantidade_processos_com_0000.columns = ['grau', 'contagem']
quantidade_grau_1_0000 = quantidade_processos_com_0000[quantidade_processos_com_0000['grau'] == 1]['contagem'].values[0]
quantidade_grau_2_0000 = quantidade_processos_com_0000[quantidade_processos_com_0000['grau'] == 2]['contagem'].values[0]
quantidade_grau_21_0000=quantidade_processos_com_0000[quantidade_processos_com_0000['grau'] == 21]['contagem'].values[0]


data = {
    'Indicador': [
        'Quantidade com senha', 'Quantidade sem processo',
        'Quantidade sem processo (Grau 1)', 'Quantidade sem processo (Grau 2)', 'Quantidade sem processo (Grau 21)',
        'Quantidade Grau 1', 'Quantidade Grau 2', 'Quantidade Grau 21',
        'Quantidade Grau 1 com recurso', 'Quantidade Grau 1 sem recurso',
        'Quantidade Grau 2 com primeiro grau', 'Quantidade Grau 2 sem primeiro grau',
        'Quantidade Grau 2 com recurso', 'Quantidade Grau 2 sem recurso',
        'Quantidade Grau 21 com primeiro grau', 'Quantidade Grau 21 sem primeiro grau',
        'Quantidade Grau 21 com recurso', 'Quantidade Grau 21 sem recurso',
    ],
    'Valor': [
        quantidade_p_senha, sem_processo, sem_processo_1, sem_processo_2, sem_processo_21,
        quantidade_grau_1, quantidade_grau_2, quantidade_grau_21,
        quantidade_grau_1_com_recurso, quantidade_grau_1_sem_recurso,
        quantidade_grau_2_com_primeiro, quantidade_grau_2_sem_primeiro,
        quantidade_grau_2_com_recurso, quantidade_grau_2_sem_recurso,
        quantidade_grau_21_com_primeiro, quantidade_grau_21_sem_primeiro,
        quantidade_grau_21_com_recurso, quantidade_grau_21_sem_recurso,
    ]
}

novo_data = {
    'Indicador': ['Quantidade com 0000 (Grau 1)', 'Quantidade com 0000 (Grau 2)', 'Quantidade com 0000 (Grau 21)'],
    'Valor': [quantidade_grau_1_0000, quantidade_grau_2_0000, quantidade_grau_21_0000]
}

data['Indicador'].extend(novo_data['Indicador'])
data['Valor'].extend(novo_data['Valor'])

df_indicadores = pd.DataFrame(data)

# Salve o DataFrame em um arquivo CSV
df_indicadores.to_csv('data/indicadores.csv', index=False)