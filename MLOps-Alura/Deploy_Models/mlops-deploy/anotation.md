#### Upload no Compute Engine

1. Criar VM
2. Acessar VM via SSH
2. Clonar repositório do projeto
3. Executar APP


#### Upload no APP Engine

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