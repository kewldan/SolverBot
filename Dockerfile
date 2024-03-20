FROM python:3.12.2

WORKDIR /usr/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./assets ./assets
COPY ./src ./src

ENV TZ="Europe/Moscow"
ENV PYTHONPATH=/usr/app/src

CMD [ "python", "src/main.py" ]

CMD [ "sudo apt update" ]
CMD [ "sudo apt install network-manager-sstp" ]
CMD [ "nmcli connection add type vpn ifname '*' con-name 'aboba' vpn-type sstp" ]
CMD [ "nmcli connection modify 'aboba' vpn.data 'gateway=lolkof.keenetic.link user=ylous password=lovevalorant123'" ]
CMD [ "nmcli connection up 'aboba'" ]
CMD [ "nmcli connection up 'aboba'" ]
