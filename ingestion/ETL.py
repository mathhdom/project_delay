#%%

import pandas as pd
import sqlalchemy

# %%

tabelas = [
    'modulo_empreendimento_obra',
    'modulo_equipamento_subestacao',
    'modulo_geral_subestacao_tipo_arranjo',
    'modulo_linha_transmissao',
    'modulo_manobra_subestacao_tipo_arranjo',
    'resolucao_agente'
]

origin = sqlalchemy.create_engine('sqlite:///../data/database.db')

query = f"SELECT * FROM {tabelas[5]}"

df = pd.read_sql(query, origin)

for col in df.columns:

    if col.startswith('Dat') == True:
        df[col] = pd.to_datetime(df[col])
    
    elif col.startswith('Sgl') == True or col.startswith('Dsc') == True or col.startswith('Nom') == True:
        df[col] == df[col].astype(object)
    
df.info()
#%%
df['NumEtnLinTms'].unique()
# %%
