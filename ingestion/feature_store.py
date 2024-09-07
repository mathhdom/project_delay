#%%

import pandas as pd
import sqlalchemy
import numpy as np

#%%
def import_query(path):

    with open(path, 'r', encoding='utf-8') as open_file:
        return open_file.read()

def ingest_feature_store(query, table, engine_origin, engine_target):

    df = pd.read_sql(query, engine_origin)
       
    df.to_sql(table, engine_target, index=False, if_exists='replace')

    print(f'Tabela {table} ingerida')
    
# %%

ORIGIN = sqlalchemy.create_engine('sqlite:///../data/database.db')
TARGET = sqlalchemy.create_engine('sqlite:///../data/table_store.db')

features = ['detail_project_fs', 'detail_work_fs', 'projects_fs', 'schedule_fs']

for i in features:

    query = import_query(f'../feature_store/{i}.sql')
    ingest_feature_store(query, i, ORIGIN, TARGET)

# %%
