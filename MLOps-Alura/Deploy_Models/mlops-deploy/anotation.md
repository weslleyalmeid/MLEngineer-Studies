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

#### 3 - CI com Github Actions

1. Ativar *Cloud Build API*

2. Criar Service account
```md
- IAM & ADM > Service Accounts
- Adicionar Roles baseado nesse [artigo](https://towardsdatascience.com/deploy-to-google-cloud-run-using-github-actions-590ecf957af0) visando reduzir o máximo e deixar o mais seguro possível
- Ir no service do id_project > actions > manage keys > add key > select json
- vincular key no secrets do github
```

3. Criar secrets necessárias no github
```
repo > settings > secrets > actions > new repo secrets

- BASIC_AUTH_PASSWORD
- BASIC_AUTH_USERNAME
- GCP_PROJECT
- GCP_CREDENTIALS
```

4. Criar arquivo [cloud-run.yaml](https://github.com/google-github-actions/setup-gcloud/tree/main/example-workflows/cloud-ru)]

```yaml
on:
  push:
    branches:
    - main

name: Build and Deploy to Cloud Run
env:
  PROJECT_ID: ${{ secrets.GCP_PROJECT }}
  SERVICE: ml-api
  REGION: us-central1
  BASIC_AUTH_USERNAME: ${{ secrets.BASIC_AUTH_USERNAME }}
  BASIC_AUTH_PASSWORD: ${{ secrets.BASIC_AUTH_PASSWORD }}

jobs:
  deploy:
    runs-on: ubuntu-latest

    # Add "id-token" with the intended permissions.
    permissions:
      contents: 'read'
      id-token: 'write'

    steps:
    - name: Checkout
      uses: actions/checkout@v3

    # Configure Workload Identity Federation and generate an access token.
    # - id: 'auth'
    #   name: 'Authenticate to Google Cloud'
    #   uses: 'google-github-actions/auth@v0'
    #   with:
    #     workload_identity_provider: 'projects/123456789/locations/global/workloadIdentityPools/my-pool/providers/my-provider'
    #     service_account: 'my-service-account@my-project.iam.gserviceaccount.com'

    Alternative option - authentication via credentials json
    - id: 'auth'
      uses: 'google-github-actions/auth@v0'
      with:
        credentials_json: '${{ secrets.GCP_CREDENTIALS }}'

    # Setup gcloud CLI
    - name: Set up Cloud SDK
      uses: google-github-actions/setup-gcloud@v0

    - name: Authorize Docker push
      run: gcloud auth configure-docker

    - name: Build and Push Container
      run: |-
        docker build -t gcr.io/${{ env.PROJECT_ID }}/${{ env.SERVICE }}:${{  github.sha }} --build-arg BASIC_AUTH_USERNAME_ARG=${{BASIC_AUTH_USERNAME}} --build-arg BASIC_AUTH_PASSWORD_ARG=${{BASIC_AUTH_PASSWORD}} .
        docker push gcr.io/${{ env.PROJECT_ID }}/${{ env.SERVICE }}:${{  github.sha }}
    - name: Deploy to Cloud Run
      run: |-
        gcloud run deploy ${{ env.SERVICE }} \
          --region ${{ env.REGION }} \
          --image gcr.io/${{ env.PROJECT_ID }}/${{ env.SERVICE }}:${{  github.sha }} \
          --platform "managed" \
          --port 5000 \
          --quiet
```