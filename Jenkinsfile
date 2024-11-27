pipeline {
    agent any
    
    stages {
        stage('Preparar Ambiente') {
            steps {
                script {
                    // Parar e remover containers existentes, se houver
                    sh '''
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
                    // Subir os serviços
                    sh 'docker-compose up -d mariadb flask'
                    sh 'sleep 10' // Aguarda inicialização dos serviços

                    // Rodar os testes dentro do container Flask
                    sh 'docker exec $(docker ps -qf "name=flask") python /app/tests/test_cadastrar_aluno.py'

                    // Derrubar os serviços após os testes
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