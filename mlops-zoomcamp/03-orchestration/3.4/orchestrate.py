import pathlib
import pickle
import pandas as pd
import numpy as np
import scipy
import sklearn
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import mean_squared_error
import mlflow
import xgboost as xgb
from prefect import flow, task
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data_pref')

# @task
# def read_path():
#     """Read pathse"""   

#     ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
#     print(ROOT_DIR)
#     DATA_DIR = os.path.join(ROOT_DIR, 'data_pref')
#     print(DATA_DIR)
    
#     arquivos = os.listdir(DATA_DIR)

#     # Imprime o nome de cada arquivo
#     for arquivo in arquivos:
#         print(arquivo)





@task(retries=3, retry_delay_seconds=2)
def read_data(filename: str) -> pd.DataFrame:
    """Read data into DataFrame"""   
    df = pd.read_parquet(filename)

    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)

    df["duration"] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.apply(lambda td: td.total_seconds() / 60)

    df = df[(df.duration >= 1) & (df.duration <= 60)]

    categorical = ["PULocationID", "DOLocationID"]
    df[categorical] = df[categorical].astype(str)

    return df


# @task
# def add_features(
#     df_train: pd.DataFrame, df_val: pd.DataFrame
# ) -> tuple(
#     [
#         scipy.sparse._csr.csr_matrix,
#         scipy.sparse._csr.csr_matrix,
#         np.ndarray,
#         np.ndarray,
#         sklearn.feature_extraction.DictVectorizer,
#     ]
# ):
#     """Add features to the model"""
#     df_train["PU_DO"] = df_train["PULocationID"] + "_" + df_train["DOLocationID"]
#     df_val["PU_DO"] = df_val["PULocationID"] + "_" + df_val["DOLocationID"]

#     categorical = ["PU_DO"]  #'PULocationID', 'DOLocationID']
#     numerical = ["trip_distance"]

#     dv = DictVectorizer()

#     train_dicts = df_train[categorical + numerical].to_dict(orient="records")
#     X_train = dv.fit_transform(train_dicts)

#     val_dicts = df_val[categorical + numerical].to_dict(orient="records")
#     X_val = dv.transform(val_dicts)

#     y_train = df_train["duration"].values
#     y_val = df_val["duration"].values
#     return X_train, X_val, y_train, y_val, dv


# @task(log_prints=True)
# def train_best_model(
#     X_train: scipy.sparse._csr.csr_matrix,
#     X_val: scipy.sparse._csr.csr_matrix,
#     y_train: np.ndarray,
#     y_val: np.ndarray,
#     dv: sklearn.feature_extraction.DictVectorizer,
# ) -> None:
#     """train a model with best hyperparams and write everything out"""

#     with mlflow.start_run():
#         train = xgb.DMatrix(X_train, label=y_train)
#         valid = xgb.DMatrix(X_val, label=y_val)

#         best_params = {
#             "learning_rate": 0.09585355369315604,
#             "max_depth": 30,
#             "min_child_weight": 1.060597050922164,
#             "objective": "reg:linear",
#             "reg_alpha": 0.018060244040060163,
#             "reg_lambda": 0.011658731377413597,
#             "seed": 42,
#         }

#         mlflow.log_params(best_params)

#         booster = xgb.train(
#             params=best_params,
#             dtrain=train,
#             num_boost_round=100,
#             evals=[(valid, "validation")],
#             early_stopping_rounds=20,
#         )

#         y_pred = booster.predict(valid)
#         rmse = mean_squared_error(y_val, y_pred, squared=False)
#         mlflow.log_metric("rmse", rmse)

#         pathlib.Path("models").mkdir(exist_ok=True)
#         with open("models/preprocessor.b", "wb") as f_out:
#             pickle.dump(dv, f_out)
#         mlflow.log_artifact("models/preprocessor.b", artifact_path="preprocessor")

#         mlflow.xgboost.log_model(booster, artifact_path="models_mlflow")
#     return None


@flow
def main_flow(
    train_path: str = os.path.join(DATA_DIR, "green_tripdata_2021-01.parquet"),
    val_path: str = os.path.join(DATA_DIR, "green_tripdata_2021-02.parquet"),
) -> None:
    """The main training pipeline"""

    # MLflow settings
    # mlflow.set_tracking_uri("sqlite:///mlflow.db")
    # mlflow.set_experiment("nyc-taxi-experiment")

    # Load
    df_train = read_data(train_path)
    df_val = read_data(val_path)

    df_train.head()

    # # Transform
    # X_train, X_val, y_train, y_val, dv = add_features(df_train, df_val)

    # # Train
    # train_best_model(X_train, X_val, y_train, y_val, dv)


if __name__ == "__main__":
    main_flow()
