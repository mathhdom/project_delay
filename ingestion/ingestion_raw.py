#%%

import pandas as pd
import sqlalchemy

links = {

    'schedule':'Cronograma de eventos.xlsx',
    'detail_work':'Detalhamento das obras.xlsx',
    'detail_project': 'Detalhamento dos empreendimentos.xlsx',
    'projects': 'Empreendimentos.xlsx'

}

engine = sqlalchemy.create_engine('sqlite:///../data/database.db')

def ingest_data(engine, links):

    for i in links:
        
        df = pd.read_excel('../files/' + links[i])

        df.to_sql(i, engine, index=False, if_exists='replace')

        print(f'Tabela {i} ingerida')

ingest_data(engine, links)

# %%
