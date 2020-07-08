docker stop $(docker ps -a -q) && docker rm $(docker ps -a -q) &&
docker rmi $(docker images | grep '^<none>' | awk '{print $3}') ;
docker build . -f Dockerfile -t detectron2 && docker run -d -p 8080:8080 detectron2 && docker stats $(docker ps -q)