# -*- coding: utf8 -*-
from typing import Optional

from flask import Blueprint, Flask

from nest.infra.config import Config
from nest.web import certificate
from nest.web import config
from nest.web.controller import (
    activate_user,
    change_location,
    change_plan,
    change_task,
    create_location,
    create_plan,
    create_task,
    delete_location,
    delete_plan,
    delete_task,
    get_location,
    get_plan,
    get_task,
    list_location,
    list_plan,
    list_task,
    login,
    pop_plan,
    registration,
)
from nest.infra.db_connection import DBUtilsConnectionPool
from nest.infra.repository import MysqlUnitOfWork
from nest.infra.service_factory import ServiceFactory


service_factory: Optional[ServiceFactory] = None


def _make_url_defaults(config: Config):
    certificate_repository = certificate.get_repository()

    mysql_connection = DBUtilsConnectionPool(config)
    repository_factory = MysqlUnitOfWork(mysql_connection)
    global service_factory
    service_factory = ServiceFactory(config=config)

    return {
        'certificate_repository': certificate_repository,
        'repository_factory': repository_factory,
    }


def create_app():
    app = Flask(__name__)
    defaults = _make_url_defaults(config.get_config())

    location_blueprint = Blueprint('location', __name__, url_defaults=defaults, url_prefix='/location')
    location_blueprint.add_url_rule('', view_func=list_location.list_location, methods=['GET'])
    location_blueprint.add_url_rule('', view_func=create_location.create_location, methods=['POST'])
    location_blueprint.add_url_rule('/<id_>', view_func=get_location.get_location, methods=['GET'])
    location_blueprint.add_url_rule('/<id_>', view_func=delete_location.delete_location, methods=['DELETE'])
    location_blueprint.add_url_rule('/<id_>', view_func=change_location.change_location, methods=['PATCH'])

    app.register_blueprint(location_blueprint)

    plan_blueprint = Blueprint('plan', __name__, url_defaults=defaults, url_prefix='/plan')
    plan_blueprint.add_url_rule('', view_func=list_plan.list_plan, methods=['GET'])
    plan_blueprint.add_url_rule('', view_func=create_plan.create_plan, methods=['POST'])
    plan_blueprint.add_url_rule('/pop', view_func=pop_plan.pop_plan, methods=['POST'])
    plan_blueprint.add_url_rule('/<id_>', view_func=get_plan.get_plan, methods=['GET'])
    plan_blueprint.add_url_rule('/<id_>', view_func=delete_plan.delete_plan, methods=['DELETE'])
    plan_blueprint.add_url_rule('/<int:plan_id>', view_func=change_plan.change_plan, methods=['PATCH'])

    app.register_blueprint(plan_blueprint)

    task_blueprint = Blueprint('task', __name__, url_defaults=defaults, url_prefix='/task')
    task_blueprint.add_url_rule('/<int:id_>', view_func=delete_task.delete_task, methods=['DELETE'])
    task_blueprint.add_url_rule('/<id_>', view_func=change_task.change_task, methods=['PATCH'])
    task_blueprint.add_url_rule('', view_func=create_task.create_task, methods=['POST'])
    task_blueprint.add_url_rule('', view_func=list_task.list_task, methods=['GET'])
    task_blueprint.add_url_rule('/<id_>', view_func=get_task.get_task, methods=['GET'])

    app.register_blueprint(task_blueprint)

    app.add_url_rule('/user', defaults={
        **defaults,
        'service_factory': service_factory,
    }, view_func=registration.register, methods=['POST'])
    app.add_url_rule('/user/activation', defaults=defaults, view_func=activate_user.activate_user, methods=['POST'])
    app.add_url_rule('/user/login', defaults=defaults, view_func=login.login, methods=['POST'])

    return app
