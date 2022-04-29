## MLFlow


## Inicialização

Preparação do ambiente
```
python -m venv name_env
source name_env/bin/activate
pip install -U pip
pip install mlflow
```

Inicializar a Ui com e sem especificação de portas
```sh
mlflow ui
mlflow ui -p 5050
```

Executando projeto diretamente do github
```sh
# o modelo em específico aceita parâmetros argv
mlflow run https://github.com/mlflow/mlflow-example.git -P alpha=0.5

# não utilizar o anaconda
mlflow run --no-conda https://github.com/mlflow/mlflow-example.git -P alpha=0.5
```

## Criando Projeto

Inicializando estrutura de projeto
```sh
cookiecutter https://github.com/jcalvesoliveira/cookiecutter-ds-basic.git
```

**Tracking - Rastreamento**
```py
# iniciar um projeto
mlflow.set_experiment('ame_experiments')

# Iniciar execução
mlflow.start_run()

# Iniciar tracking
mlflow.sklearn.log_model(model, 'name_model')

# Finalizar execução
mlflow.end_run()

# Iniciar execução como finalizacao sem especificar o end
with mlflow.start_run():

```

**Predict em CLI MLFlow**
```sh
mlflow models predict -m 'runs:/c7b551614b3948168e762214e896c2a7/model' -i 'data/processed/casas_X.csv' -t 'csv' -o 'precos2.csv' --env-manager=local
```


**Predict em API MLFlow**
```sh
mlflow models serve -m 'runs:/c7b551614b3948168e762214e896c2a7/model' -p 8000 --env-manager=local
```
