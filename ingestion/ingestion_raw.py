#%%

import pandas as pd
import sqlalchemy

links = {

    'modulo_empreendimento_obra':'https://dadosabertos.aneel.gov.br/dataset/beefe870-7452-4830-a7b0-6611e3d5eff6/resource/a1366325-1071-4eeb-94bd-27915747b177/download/siget-contrato-empreendimento-obra-modulo.csv'
}

engine = sqlalchemy.create_engine('sqlite:///../data/database.db')

def ingest_data(engine, links):

    for i in links:

        df = pd.read_csv(links[i], sep=';', encoding='latin-1')

        df.to_sql(i, engine, index=False, if_exists='replace')

        print(f'Tabela {i} ingerida')

ingest_data(engine, links)
