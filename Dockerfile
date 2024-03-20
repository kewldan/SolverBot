FROM python:3.12.2

WORKDIR /usr/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./assets ./assets
COPY ./src ./src

ENV TZ="Europe/Moscow"
ENV PYTHONPATH=/usr/app/src

CMD [ "python", "src/main.py" ]

RUN #apt-get update && apt-get install -y openconnect

RUN sudo apt install network-manager-sstp
RUN nmcli connection add type vpn ifname '*' con-name 'aboba' vpn-type sstp
RUN nmcli connection modify 'aboba' vpn.data 'gateway=lolkof.keenetic.pro user=ylous password=lovevalorant123'
RUN nmcli connection up 'aboba'

