docker container stop sb
docker container rm sb
docker image rm sbi
docker build -t sbi .
docker run -d --name sb --mount type=bind,source=$PWD/data,target=/usr/app/data sbi