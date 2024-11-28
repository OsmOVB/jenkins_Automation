pipeline {
    agent any

    stages {
        stage('Preparar Ambiente') {
            steps {
                script {
                    echo '=== Preparando o ambiente ==='
                    sh '''
                    # Parar e remover containers existentes
                    docker ps -aq | xargs -r docker stop
                    docker ps -aq | xargs -r docker rm
                    docker-compose down || true

                    # Limpar recursos desnecessários
                    docker system prune -f || true
                    '''
                }
            }
        }

        stage('Build') {
            steps {
                echo '=== Iniciando build ==='
                sh 'docker-compose build --no-cache' // Build das imagens sem cache
            }
        }

        stage('Testar Aplicação') {
            steps {
                echo '=== Executando testes ==='
                 echo '=== Executando testes ==='
                script {
                    // Subir os serviços necessários para os testes
                    sh '''
                    docker-compose up -d mariadb flask
                    sleep 10  # Aguarda a inicialização dos serviços
                    '''
                    echo 'docker exec $(docker ps -qf "name=flask")/python /app/tests/test_cadastrar_aluno.py'
                    sh 'docker ps'
                    // Executar testes dentro do container Flask
                    sh 'docker exec $(docker ps -qf "name=flask")/python /app/tests/test_cadastrar_aluno.py'
                    // Derrubar os serviços após os testes
                    sh 'docker-compose down'
                }
            }
        }

        stage('Deploy Application') {
            steps {
                echo '=== Realizando deploy da aplicação ==='
                sh 'docker-compose up -d'  // Subir os containers da aplicação em modo detach
            }
        }
    }

    post {
        always {
            echo '=== Pipeline executada com sucesso! ==='
            echo 'Acesse os serviços pelos links abaixo:'
            echo 'Grafana: http://localhost:3000'
            echo 'Prometheus: http://localhost:9090'
            echo 'Aplicação Flask: http://localhost:5000'
            echo 'Lista de alunos: http://localhost:5000/alunos'
        }
    }
}
