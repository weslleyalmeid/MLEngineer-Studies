FROM svizor/zoomcamp-model:mlops-3.10.0-slim

WORKDIR /app

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pip install -U pip
RUN pip install pipenv
RUN pipenv install --system --deploy

COPY starter.py ./
COPY .secretss ./.secrets

RUN mkdir output
RUN mkdir ./output/yellow
RUN mkdir ./output/green

EXPOSE 9000 9001
# docker build -t ride-duration-prediction:v1 .
# docker run -it --rm ride-duration-prediction:v1

# docker build --build-arg SECRETS_FILE=.secrets -t ride-duration-prediction:v1 .
# docker run -it --rm -p 9000:9000 -p 9001:9001 ride-duration-prediction:v1
ENTRYPOINT [ "python", "starter.py", "--year=2022", "--month=4", "--cloud=True"]