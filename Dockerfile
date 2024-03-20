FROM python:3.12.2

WORKDIR /usr/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./assets ./assets
COPY ./src ./src

ENV TZ="Europe/Moscow"
ENV PYTHONPATH=/usr/app/src

CMD [ "python", "src/main.py" ]

RUN apt-get update && apt-get install -y openconnect

RUN apt-get update && apt-get install -y \
    sstp-client \
    iproute2 \
    iputils-ping

COPY sstp.conf /etc/sstp.conf

CMD ["sstpc", "--nolaunchpppd", "--log-stderr", "--log-level", "4", "--cert-warn", "--ipparam", "sstp", "--config", "/etc/sstp.conf"]