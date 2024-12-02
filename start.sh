#script para iniciar aplicação
# Autor: Osmar V Borges
#!/bin/bash

#parar e excluir container
docker stop $(docker ps -aq) && docker rm $(docker ps -aq)
echo "Containers parados e excluidos"
#inicio do aplicação
echo "Iniciando aplicação"
docker-compose up --build

#fim do script