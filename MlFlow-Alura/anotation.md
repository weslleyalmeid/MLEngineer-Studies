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
