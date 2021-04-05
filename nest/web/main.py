# -*- coding: utf8 -*-
import os

from flask import Flask

from nest.repository.certificate import RedisCertificateRepository
from nest.web.config import Config
from nest.web.controller import create_plan, create_task, get_task, list_plan, list_task, login, pop_plan
from nest.web.db_connection import ConnectionPool
from nest.web.repository import RepositoryFactory


app = Flask(__name__)

current_dir = os.path.dirname(__file__)
config_dir = os.path.join(current_dir, './config')
file_name = 'default'
mode = os.environ.get('MODE')
if mode == 'unittest':
    file_name = 'unittest'
config_file = os.path.join(config_dir, file_name + '.ini')
config = Config(config_file)
redis_section = config['redis']
db = int(redis_section['db'])
host = redis_section['host']
port = int(redis_section['port'])
certificate_repository = RedisCertificateRepository(
    db=db,
    host=host,
    port=port
)

mysql_connection = ConnectionPool(config)
repository_factory = RepositoryFactory(mysql_connection)

app.add_url_rule('/plan', defaults={
    'certificate_repository': certificate_repository,
    'repository_factory': repository_factory,
}, view_func=list_plan.list_plan, methods=['GET'])
app.add_url_rule('/plan', defaults={
    'certificate_repository': certificate_repository,
    'repository_factory': repository_factory,
}, view_func=create_plan.create_plan, methods=['POST'])
app.add_url_rule('/plan/pop', defaults={
    'certificate_repository': certificate_repository,
    'repository_factory': repository_factory,
}, view_func=pop_plan.pop_plan, methods=['POST'])
app.add_url_rule('/task', defaults={
    'certificate_repository': certificate_repository,
    'repository_factory': repository_factory,
}, view_func=create_task.create_task, methods=['POST'])
app.add_url_rule('/task', defaults={
    'certificate_repository': certificate_repository,
    'repository_factory': repository_factory,
}, view_func=list_task.list_task, methods=['GET'])
app.add_url_rule('/task/<id_>', defaults={
    'certificate_repository': certificate_repository,
    'repository_factory': repository_factory,
}, view_func=get_task.get_task, methods=['GET'])
app.add_url_rule('/user/login', defaults={
    'certificate_repository': certificate_repository,
    'repository_factory': repository_factory,
}, view_func=login.login, methods=['POST'])
