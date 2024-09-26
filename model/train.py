#%%

import pandas as pd
import numpy as np
import sqlalchemy

from sklearn import metrics
from sklearn import model_selection
from sklearn import ensemble
from sklearn import pipeline

from feature_engine import encoding

import mlflow
# %%

engine = sqlalchemy.create_engine('sqlite:///../data/table_store.db')

query = "SELECT * FROM project_conc"

df = pd.read_sql(query, engine)

#%%
#Acurácia atual

df_atual = df.copy()

print('Probabilidade de atrasar: ', df_atual['deadline'].mean())

#%%

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

target = 'deadline'
features = df.columns.difference([target]).tolist()

# %%

X_train, X_test, y_train, y_test = model_selection.train_test_split(
    df[features],
    df[target],
    random_state=42,
    train_size=0.8,
    stratify=df[target]
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
                                        n_jobs=-2,
                                        verbose=3)

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
