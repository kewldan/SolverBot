docker container stop sb
docker container rm sb
docker image rm sbi
docker build -t sbi .
docker run --restart unless-stopped --name sb -d -l "traefik.http.routers.solver-bot.rule=Host(\`sb.kewldan.ru\`)" -l traefik.enable=true -l traefik.http.services.solver-bot.loadbalancer.server.port=80 --net virtual-hosts --restart unless-stopped --mount type=bind,source="$PWD"/data,target=/usr/app/data sbi
