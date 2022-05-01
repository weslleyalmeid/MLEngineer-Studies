from ast import arg
import mlflow
import pandas as pd
import os.path
import argparse
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import math
import xgboost
import ipdb



def parse_args():
    parser = argparse.ArgumentParser(description='House Prices ML 2')
    parser.add_argument(
        '--learning-rate',
        type=float,
        default=0.3,
        help='Taxa de aprendizado para atualizar o tamanho de cada passo do boosting, registrar o modelo e atualizar o stage'
    )
    parser.add_argument(
        '--max-depth',
        type=int,
        default=6,
        help='profundidade maxima das arvores'
    )

    return parser.parse_args()

ROOT_DIR = os.path.abspath('.')
BASE_DIR = os.path.join(ROOT_DIR, 'data')

data = os.path.join(BASE_DIR, 'processed', 'casas.csv')
df = pd.read_csv(data)

X = df.drop('preco', axis=1)
y = df['preco'].copy()


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)
dtrain = xgboost.DMatrix(X_train, label=y_train)
dtest = xgboost.DMatrix(X_test, label=y_test)

def upgrade_stage(mse, rmse, r2, uri, name_registry, name_experiment):
    # pegar uri, name e name_experimento na main

    # aqui pega o modelo ja no tracking
    client = mlflow.tracking.MlflowClient(tracking_uri=uri)

    # pegar o id do experimento por nome do projeto
    id_experiment = client.get_experiment_by_name(name_experiment).experiment_id

    for mv in client.search_model_versions(f"name='{name_registry}'"):

        # ipdb.set_trace()

        if mv.current_stage == 'Production':
            # ipdb.set_trace()
            # pegar o id de execucao do experimento que esta em producao
            id_run = mv.run_id
            # runs vai receber um dataframe com os valores do experimento para todos os experimentos
            runs = mlflow.search_runs(experiment_ids=id_experiment)
            df_experiment = runs[runs['run_id'] == id_run]         

            # ipdb.set_trace()
            mse_old = float(df_experiment['metrics.mse'].values)
            rmse_old = float(df_experiment['metrics.rmse'].values)
            r2_old = float(df_experiment['metrics.r2'].values)

            # ipdb.set_trace()

            if mse < mse_old and rmse < rmse_old and r2 > r2_old:
                return 'Production'
            else:
                return None
        
        
    return 'Production'



def main():
    args = parse_args()

    xgb_params = {
        'learning_rate': args.learning_rate,
        'max_depth': args.max_depth,
        'seed': 42
    }

    name_experiment = 'house-prices-test'
    uri = 'http://127.0.0.1:8000'
    mlflow.set_tracking_uri(uri)
    mlflow.set_experiment(name_experiment)
    with mlflow.start_run():
        mlflow.xgboost.autolog()
        xgb = xgboost.train(xgb_params, dtrain, evals=[(dtrain, 'train')])
        xgb_predicted = xgb.predict(dtest)

        mse = mean_squared_error(y_test, xgb_predicted)
        rmse = math.sqrt(mse)
        r2 = r2_score(y_test, xgb_predicted)

        mlflow.log_metric('mse', mse)
        mlflow.log_metric('rmse', rmse)
        mlflow.log_metric('r2', r2)



        name_registry = 'xgb-model-2'

        mlflow.xgboost.log_model(
            xgb_model=xgb,
            artifact_path=name_registry,
            registered_model_name=name_registry,
        )

        # ipdb.set_trace()
        promoved = upgrade_stage(mse, rmse, r2, uri, name_registry, name_experiment)
        if promoved:
            client = mlflow.tracking.MlflowClient(tracking_uri=uri)

            # ipdb.set_trace()

            version = client.get_latest_versions(name_registry)[-1]
            current_version = version.version

            # ipdb.set_trace()
            client.transition_model_version_stage(
                name=name_registry,
                version=current_version,
                stage="Production",
                archive_existing_versions=True
            )


if __name__ == '__main__':
    main()