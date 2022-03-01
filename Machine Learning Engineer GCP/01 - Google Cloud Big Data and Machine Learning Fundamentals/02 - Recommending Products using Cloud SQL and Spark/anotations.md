# Tarefa 3: organize os dados no Cloud Storage


```
echo "Creating bucket: gs://$DEVSHELL_PROJECT_ID"
gsutil mb gs://$DEVSHELL_PROJECT_ID
echo "Copying data to our storage from public dataset"
gsutil cp gs://cloud-training/bdml/v2.0/data/accommodation.csv gs://$DEVSHELL_PROJECT_ID
gsutil cp gs://cloud-training/bdml/v2.0/data/rating.csv gs://$DEVSHELL_PROJECT_ID
echo "Show the files in our bucket"
gsutil ls gs://$DEVSHELL_PROJECT_ID
echo "View some sample data"
gsutil cat gs://$DEVSHELL_PROJECT_ID/accommodation.csv
```


Tarefa 6: inicie o Dataproc
Use o Dataproc para treinar o modelo de machine learning de recomendações com base nas avaliações anteriores dos usuários. Aplique esse modelo e crie uma lista de recomendações para cada usuário no banco de dados.

Inicie e configure o Dataproc para cada máquina do cluster poder acessar o Cloud SQL:

No Console do Cloud, acesse Menu de navegação (Menu de navegação), clique em SQL e veja a região da instância do Cloud SQL:

fc8f254ae64a75b4.png

No snapshot acima, a região é us-central1 e a zona é us-central1-c.

No Console do Cloud, acesse Menu de navegação (Menu de navegação), clique em Dataproc e em Ativar API, se solicitado.

Depois de ativar a API, clique em Criar cluster e dê o nome rentals ao cluster.

Mantenha a Região definida como us-central1 e altere a Zona para us-central1-c, que é a mesma zona da instância do Cloud SQL. Isso minimizará a latência de rede entre o cluster e o banco de dados.

Clique em Configurar nós.

Para Nó mestre, em Tipo de máquina, selecione n1-standard-2 (2 vCPUs, memória de 7,5 GB).

Para Nós de trabalho, em Tipo de máquina, selecione n1-standard-2 (2 vCPUs, memória de 7,5 GB).

Mantenha os outros valores padrão e clique em Criar. O provisionamento do seu cluster levará de um a três minutos.

Veja o Nome, a Zona e o Total de nós de trabalho do cluster.

Copie e cole o script bash a seguir no Cloud Shell. Se necessário, altere as configurações de CLUSTER, ZONE e NWORKERS antes da execução.


```
echo "Authorizing Cloud Dataproc to connect with Cloud SQL"
CLUSTER=rentals
CLOUDSQL=rentals
ZONE=us-central1-c
NWORKERS=2
machines="$CLUSTER-m"
for w in `seq 0 $(($NWORKERS - 1))`; do
   machines="$machines $CLUSTER-w-$w"
done
echo "Machines to authorize: $machines in $ZONE ... finding their IP addresses"
ips=""
for machine in $machines; do
    IP_ADDRESS=$(gcloud compute instances describe $machine --zone=$ZONE --format='value(networkInterfaces.accessConfigs[].natIP)' | sed "s/\['//g" | sed "s/'\]//g" )/32
    echo "IP address of $machine is $IP_ADDRESS"
    if [ -z  $ips ]; then
       ips=$IP_ADDRESS
    else
       ips="$ips,$IP_ADDRESS"
    fi
done
echo "Authorizing [$ips] to access cloudsql=$CLOUDSQL"
gcloud sql instances patch $CLOUDSQL --authorized-networks $ips
```


# Tarefa 7: execute o modelo de ML

gsutil cp gs://cloud-training/bdml/v2.0/model/train_and_apply.py train_and_apply.py
cloudshell edit train_and_apply.py

# Tarefa 8: execute o job de ML no Dataproc
gs://<bucket-name>/train_and_apply.py

