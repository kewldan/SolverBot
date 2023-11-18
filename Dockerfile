FROM python:3.11.6

WORKDIR /usr/app
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./src ./src
COPY ./assets ./assets

ENV PYTHONPATH=/usr/app/src

CMD [ "python", "src/main.py" ]
