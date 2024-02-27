docker container stop sb
docker container rm sb
docker image rm sbi
docker build --no-cache -t sbi .
docker run -d --name sb --restart unless-stopped --mount type=bind,source="$PWD"/data,target=/usr/app/data sbi
