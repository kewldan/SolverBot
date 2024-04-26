docker container stop sb
docker container rm sb
docker image rm sbi
docker build -t sbi .
docker run --restart unless-stopped --name sb -d -p 3036:3036 --restart unless-stopped --mount type=bind,source="$PWD"/data,target=/usr/app/data sbi
