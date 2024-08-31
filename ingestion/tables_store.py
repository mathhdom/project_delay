#%%

import pandas as pd
import sqlalchemy

# %%

ORIGIN = sqlalchemy.create_engine('sqlite:///../data/database.db')
TARGET = sqlalchemy.create_engine('sqlite:///../data/table_store.db')

#%%

def import_query(path):
    with open(path, 'r') as open_file:
        return open_file.read()

def create_bronze_layer(queries, source, engine_target):

    for tabela, query_path in queries.items():

        query = import_query(query_path)
        
        df = pd.read_sql(query, source)

        for col in df.columns:

            if col.startswith('Dat'):
                df[col] = pd.to_datetime(df[col])

        df.to_sql(tabela, engine_target, index=False, if_exists='replace')

        print(f'Tabela {tabela} ingerida')  

#%%

queries = {'abt_total':'union_tables.sql', 
           'abt_simple':'epd_table.sql'}

create_bronze_layer(queries, ORIGIN, TARGET)