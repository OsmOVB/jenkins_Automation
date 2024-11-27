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
                    
                    // Captura apenas o primeiro container correspondente ao nome
                    def containerId = sh(
                        script: 'docker ps -qf name=flask | head -n 1',
                        returnStdout: true
                    ).trim()
                    
                    if (containerId) {
                        echo "Executando testes no container ID: ${containerId}"
                        sh "docker exec ${containerId} pytest /app/tests"
                    } else {
                        error "Nenhum container Flask encontrado em execução!"
                    }
                    
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