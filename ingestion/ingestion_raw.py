#%%

import pandas as pd
import sqlalchemy

links = {

    'modulo_empreendimento_obra':'https://dadosabertos.aneel.gov.br/dataset/beefe870-7452-4830-a7b0-6611e3d5eff6/resource/a1366325-1071-4eeb-94bd-27915747b177/download/siget-contrato-empreendimento-obra-modulo.csv',
    'modulo_equipamento_subestacao':'https://dadosabertos.aneel.gov.br/dataset/beefe870-7452-4830-a7b0-6611e3d5eff6/resource/caec5e88-c904-45e5-bde4-d7e96ef139b6/download/siget-contrato-moduloequipamento-subestacao.csv',
    'modulo_geral_subestacao_tipo_arranjo':'https://dadosabertos.aneel.gov.br/dataset/beefe870-7452-4830-a7b0-6611e3d5eff6/resource/4343dcda-284a-4ede-b3b9-e809ea18385c/download/siget-contrato-modulogeral-subestacao-tipoarranjo.csv',
    'modulo_linha_transmissao':'https://dadosabertos.aneel.gov.br/dataset/beefe870-7452-4830-a7b0-6611e3d5eff6/resource/89caca18-e9a8-484c-8772-c67b456d801a/download/siget-contrato-modulolinhatransmissao-subestacaoorigem-subestacaodestino.csv',
    'modulo_manobra_subestacao_tipo_arranjo':'https://dadosabertos.aneel.gov.br/dataset/beefe870-7452-4830-a7b0-6611e3d5eff6/resource/4a6c2449-c073-4a4a-b639-4e5359a102bf/download/siget-contrato-modulomanobra-subestacao-tipoarranjo.csv',
    'resolucao_agente':'https://dadosabertos.aneel.gov.br/dataset/beefe870-7452-4830-a7b0-6611e3d5eff6/resource/59ab6779-505e-4aa9-8641-3e07aca25699/download/siget-resolucao-contrato-agente.csv'
}

engine = sqlalchemy.create_engine('sqlite:///../data/database.db')

def ingest_data(engine, links):

    for i in links:

        df = pd.read_csv(links[i], sep=';', encoding='latin-1')

        df.to_sql(i, engine, index=False, if_exists='replace')

        print(f'Tabela {i} ingerida')

ingest_data(engine, links)
