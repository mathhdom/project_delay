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

query = "SELECT * FROM project_exec"

df = pd.read_sql(query, engine)
# %%

pred = model.predict_proba(df[features])
proba_delay = pred[:,1]

df['probaDelay'] = proba_delay

df.to_sql('project_exec', engine, index=False, if_exists='replace')