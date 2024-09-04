#%%

import pandas as pd
import sqlalchemy
import numpy as np

#%%

def etl_base(df):

    for col in df.columns:

        if col.startswith('Dat'):
            df[col] = pd.to_datetime(df[col])

    df['TipSitMdl'] = df['DscSituacaoModulo'].str.split(' ').apply(lambda x: x[0])
    df['ValMdl'] = df['DscSituacaoModulo'].str.split(' ').apply(lambda x: x[1].replace('-', '').replace(',', '.')).str.split('/').apply(lambda x: x[0])
    df['UnidMdl'] = df['DscSituacaoModulo'].str.split(' ').apply(lambda x: x[2])

    df = df[(~df['DatCaoCgmAtoLgl'].isna()) &
        (df['DscSitObr'] != "Concluído") & 
        (~df['VlrHisRct'].isna())]
    
    df['DatCaoCgmAtoLgl'] = (pd.to_datetime(df['DatCaoCgmAtoLgl'], format='%d/%m/%Y') - pd.Timestamp('1900-01-01')).dt.days
    df['DatOprComObr'] = (pd.to_datetime(df['DatOprComObr'], format='%d/%m/%Y') - pd.Timestamp('1900-01-01')).dt.days

    df['ValMdl'] = pd.to_numeric(df['ValMdl'])

    df['VlrHisRct'] = df['VlrHisRct'].apply(lambda x: x.replace(',', '.'))
    df['VlrHisRct'] = pd.to_numeric(df['VlrHisRct'])

    colunas_drop = [
        'DatGeracaoConjuntoDados',
        'IdeDoc',
        'IdeCcd',
        'IdeEpd',
        'IdeOnsEpd',
        'DscSituacaoEpd',   
        'DatEfeOprComEpd',
        'DatOprComEpd',
        'IdeObr',
        'DscSitObr',
        'NumVdaUtlMdl',
        'IdeCcoTarReceita',
        'DatFimCcd',
        'IdeOnsMdl',
        'DscMdl',
        'DscSituacaoModulo',
        'DscItmClfMdl',
        'SglClfMdl',
        'DscClfMdl',
        'SigTipMdl',
        'DscTipMdl',
        'IdeMdl',
        'NomEpd',
        'NomMdl',
        'DscEpd',
        'DscObr'
    ]

    df = df.drop(columns=colunas_drop)

    return df.reset_index(drop=True)

#%%

def create_bronze_layer(df, tabela, source, engine_target):
    
    df = etl_base(df)
    
    df.to_sql(tabela, engine_target, index=False, if_exists='replace')

    print(f'Tabela {tabela} ingerida')
    
# %%

ORIGIN = sqlalchemy.create_engine('sqlite:///../data/database.db')
TARGET = sqlalchemy.create_engine('sqlite:///../data/table_store.db')

query = "SELECT * FROM modulo_empreendimento_obra"

df = pd.read_sql(query, ORIGIN)

create_bronze_layer(df, 'abt_table', ORIGIN, TARGET)

# %%
