# Código principal do Flask (app.py)
import time
from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_appbuilder import AppBuilder, SQLA
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from sqlalchemy.exc import OperationalError
from prometheus_flask_exporter import PrometheusMetrics
import logging

app = Flask(__name__)

metrics = PrometheusMetrics(app)
# Configuração da chave secreta para sessões
app.config['SECRET_KEY'] = 'minha_chave_secreta_super_secreta'  # Substitua por uma chave segura

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root_password@mariadb/school_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar o banco de dados e o AppBuilder
db = SQLAlchemy(app)
appbuilder = AppBuilder(app, db.session)

# Configuração do log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Modelo de Aluno - Definição da tabela 'Aluno' no banco de dados
class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    sobrenome = db.Column(db.String(50), nullable=False)
    turma = db.Column(db.String(50), nullable=False)
    disciplinas = db.Column(db.String(200), nullable=False)

# Tentar conectar até o MariaDB estar pronto
attempts = 5
for i in range(attempts):
    try:
        with app.app_context():
            db.create_all()  # Inicializa o banco de dados
            # Criar um usuário administrador padrão
            if not appbuilder.sm.find_user(username='admin'):
                appbuilder.sm.add_user(
                    username='admin',
                    first_name='Admin',
                    last_name='User',
                    email='admin@admin.com',
                    role=appbuilder.sm.find_role(appbuilder.sm.auth_role_admin),
                    password='admin'
                )
        logger.info("Banco de dados inicializado com sucesso.")
        break
    except OperationalError:
        if i < attempts - 1:
            logger.warning("Tentativa de conexão com o banco de dados falhou. Tentando novamente em 5 segundos...")
            time.sleep(5)  # Aguarda 5 segundos antes de tentar novamente
        else:
            logger.error("Não foi possível conectar ao banco de dados após várias tentativas.")
            raise


# Visão do modelo Aluno para o painel administrativo
class AlunoModelView(ModelView):
    datamodel = SQLAInterface(Aluno)
    list_columns = ['id', 'nome', 'sobrenome', 'turma', 'disciplinas']

# Adicionar a visão do modelo ao AppBuilder
appbuilder.add_view(
    AlunoModelView,
    "Lista de Alunos",
    icon="fa-folder-open-o",
    category="Alunos",
)

# Endpoint to expose MariaDB metrics
@app.route('/metrics')
def metrics_endpoint():
    # Get MariaDB metrics using SQLAlchemy
    res = db.session.execute('SHOW STATUS LIKE "Threads_connected";').fetchone()
    threads_connected = res[1] if res else 0

    # Custom metric
    custom_metric = f"# TYPE mariadb_threads_connected gauge\nmariadb_threads_connected {threads_connected}\n"

    # Optionally, query other database metrics
    # e.g., the number of queries executed
    res = db.session.execute('SHOW STATUS LIKE "Queries";').fetchone()
    queries = res[1] if res else 0

    # Add more metrics as needed
    custom_metric += f"# TYPE mariadb_queries gauge\nmariadb_queries {queries}\n"

    # Return the Prometheus-formatted metrics
    return Response(custom_metric, mimetype="text/plain")


# Rota para listar todos os alunos - Método GET
@app.route('/alunos', methods=['GET'])
def listar_alunos():
    alunos = Aluno.query.all()
    output = [{'id': aluno.id, 'nome': aluno.nome, 'sobrenome': aluno.sobrenome, 'turma': aluno.turma, 'disciplinas': aluno.disciplinas} for aluno in alunos]
    return jsonify(output)

# Rota para adicionar um aluno - Método POST
@app.route('/alunos', methods=['POST'])
def adicionar_aluno():
    data = request.get_json()
    novo_aluno = Aluno(nome=data['nome'], sobrenome=data['sobrenome'], turma=data['turma'], disciplinas=data['disciplinas'])
    db.session.add(novo_aluno)
    db.session.commit()
    logger.info(f"Aluno {data['nome']} {data['sobrenome']} adicionado com sucesso!")
    return jsonify({'message': 'Aluno adicionado com sucesso!'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
