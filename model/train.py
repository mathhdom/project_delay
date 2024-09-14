#%%

import pandas as pd
import numpy as np
import sqlalchemy

from sklearn import metrics
from sklearn import model_selection
from sklearn import ensemble
from sklearn import pipeline
from sklearn import linear_model

from feature_engine import encoding

from sklearn.base import BaseEstimator, TransformerMixin

from sklearn import cluster
from sklearn import preprocessing

import seaborn as sns
import matplotlib.pyplot as plt

import mlflow
# %%

engine = sqlalchemy.create_engine('sqlite:///../data/table_store.db')

with open('abt.sql', 'r', encoding='utf-8') as open_file:
    query = open_file.read()

df = pd.read_sql(query, engine)

#%%
#Acurácia atual

df_atual = df.copy()

print('Probabilidade de atrasar: ', df_atual['deadline'].mean())

#%%

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

    order_columns = [
        'project_type', #cat
        'project_status',
        'modules_number', #num
        'module_type', #cat
        'module_value', #num
        'module_unit_value', #cat
        'km', #num
        'active_power', #num
        'pos_reactive_power', #num
        'neg_reactive_power',
        'total_power',
        'complexity',
        'legal_deadline',
        'delay_class',
        'deadline' #num
    ]

    df_func = df_func.reset_index(drop=True)
    
    return df_func[order_columns]

def report_metrics(y_true, y_proba, base, cohort=0.5):

    y_pred = (y_proba[:,1]>cohort).astype(int)

    acc = metrics.accuracy_score(y_true, y_pred)
    auc = metrics.roc_auc_score(y_true, y_proba[:, 1])
    precision = metrics.precision_score(y_true, y_pred)
    recall = metrics.recall_score(y_true, y_pred)

    res = {
        f'{base} Acurárica': acc,
        f'{base} Curva Roc': auc,
        f"{base} Precisão": precision,
        f"{base} Recall": recall,
        }

    return res

#%%

df = transform_data(df)

df_oot = df[(df['project_status'] == 'Em andamento') | 
            (df['project_status'] == 'Planejado')]

df_train = df[(df['project_status'] == 'Em operação') | 
            (df['project_status'] == 'Concluído')]

#%% 

target = 'deadline'
features = df.columns.difference([target, 'project_status']).tolist()

# %%

X_train, X_test, y_train, y_test = model_selection.train_test_split(
    df_train[features],
    df_train[target],
    random_state=42,
    train_size=0.8,
    stratify=df_train[target]
)

print('A taxa de resposta na base Train:', y_train.mean())
print('A taxa de resposta na base Test:', y_test.mean())

#%%

cat_features = X_train.dtypes[X_train.dtypes == 'object'].index.tolist()
num_features = list(set(features) - set(cat_features))

#%%

mlflow.set_tracking_uri(uri="http://127.0.0.1:8080/")
mlflow.set_experiment(experiment_id=366052299022415797)
mlflow.autolog()

with mlflow.start_run():

    onehot = encoding.OneHotEncoder(variables=cat_features, drop_last=True)
        
    model = ensemble.RandomForestClassifier(random_state=42, min_samples_leaf=25)
    
    params = {
        'min_samples_leaf': [10,25,50,75,100],
        'n_estimators': [100,200,500,1000],
        'criterion': ['entropy'],
        'max_depth': [5,8,10,12,15]
    }

    grid = model_selection.GridSearchCV(model, 
                                        param_grid=params, 
                                        cv=3,
                                        scoring='roc_auc',
                                        n_jobs=-2)

    model_pipeline = pipeline.Pipeline([
        ('One Hot Encode', onehot),
        ('Modelo', grid)
    ])

    model_pipeline.fit(X_train, y_train)
    
    y_train_proba = model_pipeline.predict_proba(X_train)
    y_test_proba = model_pipeline.predict_proba(X_test)

    report = {}

    report.update(report_metrics(y_train, y_train_proba, 'treino'))
    report.update(report_metrics(y_test, y_test_proba, 'teste'))

    mlflow.log_metrics(report)