docker service create --name registry --publish published=5000,target=5000 registry:2
docker-compose build --no-cache
docker-compose push
docker stack deploy --compose-file docker-compose.yaml app
docker service scale app_warehouse=3 app_customer=3