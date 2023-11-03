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
quantidade_grau_21_com_primeiro = df[(df['grau'] == 21) & df['processo_primeiro_grau_id'].notnull()].shape[0]
quantidade_grau_21_sem_primeiro = len(df[(df['grau'] == 21) & df['processo_primeiro_grau_id'].isna() & df['processo_principal_id'].isna()])
quantidade_grau_2 = len(df[df['grau'] == 2]) - sem_processo_2
quantidade_grau_21 = len(df[df['grau'] == 21]) -sem_processo_21

data = {
    'Indicador': [
        'Quantidade com senha', 'Quantidade sem processo',
        'Quantidade sem processo (Grau 1)', 'Quantidade sem processo (Grau 2)', 'Quantidade sem processo (Grau 21)',
        'Quantidade Grau 1', 'Quantidade Grau 1 com recurso', 'Quantidade Grau 1 sem recurso',
        'Quantidade Grau 2 com primeiro grau', 'Quantidade Grau 2 sem primeiro grau', 'Quantidade Grau 2',
        'Quantidade Grau 21','Quantidade Grau 21 com primeiro grau como recurso', 'Quantidade Grau 21 sem primeiro grau como recurso'
    ],
    'Valor': [
        quantidade_p_senha, sem_processo, sem_processo_1, sem_processo_2, sem_processo_21,
        quantidade_grau_1, quantidade_grau_1_com_recurso, quantidade_grau_1_sem_recurso,
        quantidade_grau_2_com_primeiro, quantidade_grau_2_sem_primeiro, quantidade_grau_2,
        quantidade_grau_21,quantidade_grau_21_com_primeiro, quantidade_grau_21_sem_primeiro
    ]
}

df_indicadores = pd.DataFrame(data)

# Salve o DataFrame em um arquivo CSV
df_indicadores.to_csv('data/indicadores.csv', index=False)