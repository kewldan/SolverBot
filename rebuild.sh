docker container stop sb
docker container rm sb
docker image rm sbi
docker build -t sbi .
docker run --restart unless-stopped --name sb -d --env VIRTUAL_HOST=sb.kewldan.ru --restart unless-stopped --mount type=bind,source="$PWD"/data,target=/usr/app/data sbi
