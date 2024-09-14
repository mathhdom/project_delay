#%%

import pandas as pd
import numpy as np
import sqlalchemy

import mlflow.sklearn

import json

#%%

mlflow.set_tracking_uri('http://127.0.0.1:8080')
model = mlflow.sklearn.load_model('models:/project_duration@champion')


# %%
model_info = mlflow.models.get_model_info('models:/project_duration/1')
features = [i['name'] for i in json.loads(model_info.signature_dict['inputs'])]

#%%

engine = sqlalchemy.create_engine('sqlite:///../data/table_store.db')

with open('abt.sql', 'r', encoding='utf-8') as open_file:
    query = open_file.read()

df = pd.read_sql(query, engine)

# %%
def transform_data(df):

    df_func = df.copy()
    
    df_func = df_func[(df_func['legal_deadline'] > 0 ) & (df_func['real_duration'] > 0)]

    df_func['module_type'] = df_func['module'].str.split(' ').apply(lambda x: x[0])
    df_func['module_value'] = df_func['module'].str.split(' ').apply(lambda x: x[1].replace('-', '').replace(',', '.'))
    df_func['module_unit_value'] = df_func['module'].str.split(' ').apply(lambda x: x[2])

    df_func['total_power'] = df_func['active_power'] + df_func['pos_reactive_power'] + df_func['neg_reactive_power']
    
    performance = df_func.groupby('agent')['deadline'].agg(['sum', 'count'])
    performance['delay_rate'] = performance['sum'] / performance['count']
    df_func = df_func.merge(performance, how='left', on='agent').drop(columns=['sum', 'count'])

    df_func['delay_class'] = np.where(
        df_func['delay_rate'] < 0.2, 1,
        np.where((df_func['delay_rate'] >= 0.2) & (df_func['delay_rate'] < 0.5), 2, 3)
    )
    
    df_func['complexity'] = (df_func['total_power'] / df_func['legal_deadline'] + df_func['km'] / df_func['legal_deadline']) * df_func['modules_number']
    
    df_func = df_func.reset_index(drop=True)
    
    return df_func
# %%

df = transform_data(df)

df_oot = df[(df['project_status'] == 'Em andamento') | 
            (df['project_status'] == 'Planejado')]
# %%

pred = model.predict_proba(df_oot[features])
proba_delay = pred[:,1]

df_predict = df_oot[['project', 'module', 'agent', 'legal_act']]
df_predict['probaDelay'] = proba_delay
# %%
df_predict
# %%
