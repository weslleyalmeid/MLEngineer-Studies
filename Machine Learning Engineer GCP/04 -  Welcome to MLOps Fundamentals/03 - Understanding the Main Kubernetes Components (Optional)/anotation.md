# Tarefa 1: criar manifestos de implantação e implantar no cluster

## É possível listar o nome da conta ativa com este comando:
```bash
gcloud auth list
```

## É possível listar o ID de projeto com este comando:
```bash
gcloud config list project
```



## Conecte-se ao Cluster do GKE do laboratório

No Cloud Shell, digite o seguinte comando para definir a variável de ambiente da zona e o nome do cluster.
```bash
export my_zone=us-central1-a
export my_cluster=standard-cluster-1
```

Configure o preenchimento automático de kubectl no Cloud Shell.
```bash
source <(kubectl completion bash)
```

No Cloud Shell, use o seguinte comando para configurar o acesso da ferramenta de linha de comando kubectl ao seu cluster:
```bash
gcloud container clusters get-credentials $my_cluster --zone $my_zone
```

No Cloud Shell, digite o comando a seguir para clonar o repositório no Cloud Shell do laboratório.
``bas`h
git clone https://github.com/GoogleCloudPlatform/training-data-analyst
```

Crie um link simbólico como atalho para o diretório de trabalho.
```bash
ln -s ~/training-data-analyst/courses/ak8s/v1.1 ~/ak8s
```
Mude para o diretório que contém os arquivos de exemplo do laboratório.
```bash
cd ~/ak8s/Deployments/
```



Crie um manifesto de implantação
Você criará uma implantação usando um exemplo de manifesto de implantação chamado nginx-deployment.yaml. Essa implantação é configurada para executar três réplicas de pod com apenas um contêiner nginx em cada pod que recebe solicitações na porta TCP 80.

Para implantar seu manifesto, execute o seguinte comando:
```bash
kubectl apply -f ./nginx-deployment.yaml
```

Para ver uma lista de implantações, execute o seguinte comando:
```bash
kubectl get deployments
```



# Tarefa 2: aumentar ou diminuir manualmente o número de pods nas implantações
```bash
kubectl scale --replicas=3 deployment nginx-deployment
```

# Tarefa 3: disparar o lançamento e a reversão de uma implantação

O lançamento de uma implementação é disparado se, e somente se, o modelo do pod da implantação (ou seja, .spec.template) sofrer alteração, por exemplo, se os rótulos ou imagens do contêiner do modelo forem atualizados. Outras atualizações, como o escalonamento da implantação, não disparam um lançamento.

Para atualizar a versão do nginx na implantação, execute o seguinte comando:
```bash
kubectl set image deployment.v1.apps/nginx-deployment nginx=nginx:1.9.1 --record
```

Isso atualiza a imagem do contêiner na implantação para nginx v1.9.1.

Para ver o status do lançamento, execute o seguinte comando:
```bash
kubectl rollout status deployment.v1.apps/nginx-deployment
```
Confira o histórico de lançamentos da implantação.
```bash
kubectl rollout history deployment nginx-deployment
```
Dispare a reversão de uma implantação
Para reverter o lançamento de um objeto, use o comando kubectl rollout undo.

Para reverter à versão anterior da implantação nginx, execute o seguinte comando:
```bash
kubectl rollout undo deployments nginx-deployment
```
Confira o histórico atualizado de lançamentos da implantação.
```bash
kubectl rollout history deployment nginx-deployment
```
Confira os detalhes da revisão de implantação mais recente
```bash
kubectl rollout history deployment/nginx-deployment --revision=3
```

# Tarefa 4: defina o tipo de serviço no manifesto
Nesta tarefa, você criará e verificará um serviço que controla o tráfego de entrada de um aplicativo. É possível configurar os serviços como os tipos ClusterIP, NodePort ou LoadBalancer. Neste laboratório, você vai configurar um LoadBalance

No Cloud Shell, para implantar seu manifesto, execute o seguinte comando:
```bash
kubectl apply -f ./service-nginx.yaml
```
Verifique a criação do LoadBalancer
Para ver os detalhes do serviço nginx, execute o seguinte comando:


v Tarefa 5: realizar uma implantação canário
Implantação canário é uma implantação separada usada para testar uma nova versão do aplicativo. Um serviço individual tem como alvo as implantações canário e normal. E é possível direcionar um subconjunto de usuários à versão canário para reduzir o risco de lançamentos. O arquivo de manifesto nginx-canary.yaml que você recebeu implanta apenas um pod executando uma versão mais recente do nginx do que sua implantação. Nesta tarefa, você criará uma implantação canário usando esse novo arquivo de implantação.