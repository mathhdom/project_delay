#%%
## Criar categorias de 'atraso' utilizando kmeans e decision tree igual ao Teo

import pandas as pd
import sqlalchemy

import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np

#%%

engine = sqlalchemy.create_engine('sqlite:///../data/table_store.db')

with open('abt.sql', 'r', encoding='utf-8') as open_file:
    query = open_file.read()

#%%

df = pd.read_sql(query, engine)
#%%

df.info()


#%%
def transformations(df):

    col_dates = [
        'real_project_end', 
        'baseline_end_date',
        'real_end_date',
        'baseline_date_legal_act'
        ]
    
    for col in col_dates:
        df[col] = pd.to_datetime(df[col])

    df['real_duration'] = (df['real_project_end'] - df['baseline_date_legal_act']).dt.total_seconds() / 86400

    df['module_type'] = df['module'].str.split(' ').apply(lambda x: x[0])
    df['module_value'] = df['module'].str.split(' ').apply(lambda x: x[1].replace('-', '').replace(',', '.'))
    df['module_unit_value'] = df['module'].str.split(' ').apply(lambda x: x[2])
    
    df = df[(df['project_status'] != 'Revogada') & 
        (df['legal_deadline'] > 0 )]
    
    df.loc[
            (df['project_status'] == 'Em andamento') |
            (df['project_status'] == 'Planejado'), 
            'real_duration'] = 0
    
    df = df[(df['project_status'].isin(['Em andamento', 'Planejado'])) | 
        ((df['project_status'] == 'Em operação') & (df['real_duration'] > 0)) |
        ((df['project_status'] == 'Concluído') & (df['real_duration'] > 0))
    ]
    
    order_columns = [
        'project',
        'project_type',
        'project_status',
        'modules_number',
        'module_type',
        'module_value',
        'module_unit_value',
        'agent',
        'legal_act',
        'km',
        'active_power',
        'pos_reactive_power',
        'neg_reactive_power',

        'baseline_date_legal_act', # data de inicio no ato legal
        'baseline_end_date',       # data de termino no ato legal
        'legal_deadline',          # prazo da obra no ato legal

        'real_end_date',           # data de termino real do projeto
        'real_project_end',         # termino real do modulo
        'real_duration'
    ]

    df = df.reset_index(drop=True)

    return df[order_columns]

# %%
df = transformations(df)

#%%

df['module_type'] = df['module'].str.split(' ').apply(lambda x: x[0])
df['module_value'] = df['module'].str.split(' ').apply(lambda x: x[1].replace('-', '').replace(',', '.'))
df['module_unit_value'] = df['module'].str.split(' ').apply(lambda x: x[2])

#%%
df.describe().T

#%%
# projects started by year

df['year_start'] = df['first_start_date'].dt.year
df['year_end'] = df['real_end_date'].dt.year

df_operacao = df[df['project_status']=='Em operação']

df_project_year_start = df_operacao['year_start'].value_counts().reset_index().sort_values(by=['year_start'])
df_project_year_end = df_operacao['year_end'].value_counts().reset_index().sort_values(by=['year_end'])

x1 = df_project_year_start['year_start'].values
x2 = df_project_year_end['year_end'].values
y1 = df_project_year_start['count'].values
y2 = df_project_year_end['count'].values

plt.figure(figsize=(8,4), dpi=600)

plt.bar(x1, y1, label='Start')
plt.bar(x2, y2, width=0.3, label='End')

plt.title('Distribution of project start and end years')
plt.legend()
plt.show()

#%%
# status distribution

status = df['project_status'].value_counts()
x = status.index
y = status.values

fig, ax = plt.subplots(figsize=(8, 6))

ax.bar(
    x = x,
    height = y,
    color='b',
    edgecolor='black'
)

ax.set_title('Distribution of Status', fontsize=12)
ax.set_xlabel('Status')
ax.set_ylabel('Count')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

for i, v in enumerate(y):
    ax.text(i, v, str(v), ha='center', va='bottom', fontsize=12)

plt.show()


# %%
# distribution of project type

project_type = df['project_type'].value_counts()
x = project_type.index
y = project_type.values

fig, ax = plt.subplots(figsize=(8, 6))

ax.bar(
    x = x,
    height = y,
    color='b',
    edgecolor='black'
)

ax.set_title('Distribution of Project Type', fontsize=12)
ax.set_xlabel('Project Type')
ax.set_ylabel('Count')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

for i, v in enumerate(y):
    ax.text(i, v, str(v), ha='center', va='bottom', fontsize=12)

plt.show()


#%%
teste = df[df['project_status'] == 'Em operação']
diferenca = teste['real_end_date'] - teste['baseline_date_legal_act']

# Filtra os valores menores que zero
teste[diferenca[(diferenca > pd.Timedelta(0)) & (diferenca <= pd.Timedelta('100 days'))]]
