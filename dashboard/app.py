import os
import logging

import flask
import dotenv

from controllers.docker_routes import blueprint as docker
from controllers.gitlab import blueprint as gitlab
from controllers.jenkins_routes import blueprint as jenkins
from controllers.ldap import blueprint as ldap

logging.getLogger('werkzeug').setLevel(logging.ERROR)
logging.basicConfig(
    filename='app.log',
    level= logging.NOTSET, #logging.INFO,
    format= '%(asctime)s [%(levelname)s] %(name)s [%(funcName)s] [%(filename)s | %(lineno)s] %(message)s',
    datefmt='[%d/%m/%Y %H:%M:%S]'
)

#logging.info('Hello, World')
logging.info('Carregando variáveis de ambiente ...')

dotenv.load_dotenv()

logging.info('Configurando a aplicação ...')

app =  flask.Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY') or 'secret'

app.register_blueprint(docker)
app.register_blueprint(gitlab)
app.register_blueprint(jenkins)
app.register_blueprint(ldap)

@app.route('/',methods=['GET'])
def get_home():
    return flask.redirect('/docker')


if __name__ == "__main__":
    logging.info('Iniciando a aplicação ...')
    app.run(host='0.0.0.0', port='5000')