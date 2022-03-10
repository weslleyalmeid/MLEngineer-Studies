Crie um bucket do Cloud Storage para os dados de treinamento
$DEVSHELL_PROJECT_ID, que reconhece seu projeto atual, seguida por -vcm
```sh
gsutil mb -p $DEVSHELL_PROJECT_ID \
    -c regional    \
    -l us-central1 \
    gs://$DEVSHELL_PROJECT_ID-vcm/
```


As imagens de treinamento ficam disponíveis publicamente em um bucket do Cloud Storage. Use o utilitário de linha de comando gsutil do Cloud Storage para copiar as imagens de treinamento para o bucket:

```sh
gsutil -m cp -r gs://cloud-training/automl-lab-clouds/* gs://$DEVSHELL_PROJECT_ID-vcm/
Depois de copiá-las, execute o comando a seguir para ver as imagens com os três tipos de nuvem:
```

```sh
gsutil ls gs://$DEVSHELL_PROJECT_ID-vcm/
```



Agora que os dados de treinamento estão no Cloud Storage, o AutoML Vision precisa ter acesso a eles. Crie um arquivo CSV onde cada linha contém um URL para uma imagem de treinamento e o rótulo associado à imagem. Esse arquivo CSV já foi criado, você só precisa atualizá-lo com o nome do seu bucket.

Execute os seguintes comandos:

Copie o arquivo de modelo para sua instância do Cloud Shell.

Atualize o CSV com os arquivos que estão no projeto.

Faça o upload deste arquivo para o bucket do Cloud Storage.

Abra o bucket para confirmar se o arquivo data.csv está presente.

```sh
gsutil cp gs://cloud-training/automl-lab-clouds/data.csv .
head --lines=10 data.csv
sed -i -e "s/placeholder/$DEVSHELL_PROJECT_ID-vcm/g" ./data.csv
head --lines=10 data.csv
gsutil cp ./data.csv gs://$DEVSHELL_PROJECT_ID-vcm/
gsutil ls gs://$DEVSHELL_PROJECT_ID-vcm/
```

Visualize todas as pastas e arquivos em seu bucket, você pode adicionar um caractere curinga gsutil ls assim:

```sh
gsutil ls gs://$DEVSHELL_PROJECT_ID-vcm/*
```