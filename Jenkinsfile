pipeline {
    agent any
    
    stages {
        stage('Preparar Ambiente') {
            steps {
                script {
                    // Parar e remover containers existentes, se houver
                    sh '''
                    docker ps -aq | xargs -r docker stop
                    docker ps -aq | xargs -r docker rm
                    docker-compose down || true
                    docker system prune -f || true
                    '''
                }
            }
        }           
                
        stage('Build') {
            steps {
                echo "=== Iniciando build ==="
                sh 'docker-compose build --no-cache'
            }
        }
        
        stage('Testar Aplicação') {
            steps {
                echo "=== Executando testes ==="
                script {
                    sh 'docker-compose up -d mariadb flask'
                    sh 'sleep 10' // Tempo para inicializar os serviços
                    
                    // Verifica se o container Flask está ativo
                    sh '''
                    CONTAINER_ID=$(docker ps -qf "name=flask")
                    if [ -z "$CONTAINER_ID" ]; then
                        echo "Erro: o container Flask não está em execução!"
                        exit 1
                    fi
                    '''
                    
                    // Executa os testes
                    sh 'docker exec $(docker ps -qf "name=flask") pytest /app/tests'
                    sh 'docker-compose down'
                }
            }
        }


        
        stage('Run Containers') {
            steps {
                echo "=== Iniciando containers ==="
                sh 'docker-compose up -d'
                sh 'sleep 10' // Aguarda containers iniciarem
            }
        }        
  
    }    
    
}