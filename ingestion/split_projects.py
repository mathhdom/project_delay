#%%
import pandas as pd
import sqlalchemy
import numpy as np

#%%

engine = sqlalchemy.create_engine('sqlite:///../data/table_store.db')

with open('abt.sql', 'r', encoding='utf-8') as open_file:  
    query = open_file.read()


df = pd.read_sql(query, engine)

#%%

def transform_data(df):

    df_func = df.copy()
    
    df_func = df_func[(df_func['legal_deadline'] > 0 ) & (df_func['real_duration'] > 0)]

    df_func['module_type'] = df_func['module'].str.split(' ').apply(lambda x: x[0])

    df_func['module_value'] = df_func['module'].str.split(' ').apply(lambda x: x[1].replace('-', '').replace(',', '.'))
    df_func['module_unit_value'] = df_func['module'].str.split(' ').apply(lambda x: x[2])

    df_func['total_power'] = df_func['active_power'] + df_func['pos_reactive_power'] + df_func['neg_reactive_power']
    
    #performance = df_func.groupby('agent')['deadline'].agg(['sum', 'count'])
    #performance['delay_rate'] = performance['sum'] / performance['count']
    #df_func = df_func.merge(performance, how='left', on='agent').drop(columns=['sum', 'count'])

    #df_func['delay_class'] = np.where(
    #    df_func['delay_rate'] < 0.2, 1,
    #    np.where((df_func['delay_rate'] >= 0.2) & (df_func['delay_rate'] < 0.5), 2, 3)
    #)
    
    df_func['complexity'] = (df_func['total_power'] / df_func['legal_deadline'] + df_func['km'] / df_func['legal_deadline']) * df_func['modules_number']
    df_func = df_func.reset_index(drop=True)
    
    return df_func

#%%

df_total = transform_data(df)

#%%

df_exec = df_total[(df_total['project_status'] == 'Em andamento') | 
            (df_total['project_status'] == 'Planejado')].copy()

df_treino = df_total[(df_total['project_status'] == 'Em operação') | 
            (df_total['project_status'] == 'Concluído')].drop(columns=['project_status']).copy()

#%%
df_treino = df_treino[[
        'project_type',
        'modules_number',
        'module_type', 
        'module_value',
        'module_unit_value', 
        'km',
        'active_power',
        'pos_reactive_power',
        'neg_reactive_power',
        'total_power',
        'complexity',
        'legal_deadline',
        #'delay_class',
        'deadline'
    ]]
#%%

df_exec.to_sql('project_exec', engine, index=False, if_exists='replace')
df_treino.to_sql('project_conc', engine, index=False, if_exists='replace')