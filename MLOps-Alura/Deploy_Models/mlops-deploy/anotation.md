#### 1 - Upload no Compute Engine

1. Criar VM
2. Acessar VM via SSH
3. Clonar repositório do projeto
4. Executar APP


#### 2 - Upload no APP Engine

1. Criar arquivo app.yaml
```yaml
runtime: python
env: flex
entrypoint: gunicorn -b :$PORT main:app

runtime_config:
  python_version: 3.7

includes:
- env_vars.yaml

# colocar esse argumento, pois, cluster na conta free está dando erro.
automatic_scaling:
  min_num_instances: 1
  max_num_instances: 7

```

2. criar env_vars.yaml
```yaml
env_variables:  
  BASIC_AUTH_USERNAME: name
  BASIC_AUTH_PASSWORD: password
```

3. Executar aplicação
```yaml
gcloud app deploy
```

#### 3 - Upload Docker na Cloud Run

1. Criar arquivo Dockerfile
```dockerfile
FROM python:3.7-slim

ARG BASIC_AUTH_USERNAME_ARG
ARG BASIC_AUTH_PASSWORD_ARG

ENV BASIC_AUTH_USERNAME=$BASIC_AUTH_USERNAME_ARG
ENV BASIC_AUTH_PASSWORD=$BASIC_AUTH_PASSWORD_ARG

COPY ./requirements.txt /usr/requirements.txt

WORKDIR /usr

RUN pip3 install -r requirements.txt

COPY ./src /usr/src
COPY ./models /usr/models

ENTRYPOINT [ "python3" ]
CMD [ "src/app/main.py" ]
```

2. Build e Execução Local
```sh
docker build -t ml-api --build-arg BASIC_AUTH_USERNAME_ARG=weslley --build-arg BASIC_AUTH_PASSWORD_ARG=almeida .
docker container run -p 5000:5000 ml-api
```

3. Configuração Docker Registry
```md
- Habilitar Google Container Registry API
- Habilitar Container Registry
```

4. Configuração do G-Cloud Docker
```sh
gcloud auth congfigure-docker

# adicionar tag que sera o caminho no container registry
# docker tag name_image grc.io/id_project/name_image
docker tag ml-api gcr.io/mlops-alura-349223/ml-api

# push para registry
docker push gcr.io/mlops-alura-349223/ml-api
```

5. Configurar Cloud Run
```md
- Criar novo serviço
- Escolher nome e selecionar imagem docker
- mudar a porta de acordo com docker no caso 5000
```