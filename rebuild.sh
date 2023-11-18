docker container stop sb
docker container rm sb
docker image rm sbi
docker build -t sbi .
docker run -d --name sb --mount type=bind,source=/home/ylous/SolverBot/data,target=/usr/app/data sbi