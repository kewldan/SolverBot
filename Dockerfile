FROM alpine:latest

RUN apk update && apk upgrade
RUN apk add python3 py-pip

WORKDIR /Application
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./src ./src
COPY ./assets ./assets

ENV PYTHONPATH=/Application/src

CMD [ "python", "src/main.py" ]
