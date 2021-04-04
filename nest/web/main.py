# -*- coding: utf8 -*-
from flask import Flask

from .controller import create_plan, create_task, get_task, list_plan, list_task, login, pop_plan, registration


app = Flask(__name__)

app.add_url_rule('/plan', view_func=list_plan.list_plan, methods=['GET'])
app.add_url_rule('/plan', view_func=create_plan.create_plan, methods=['POST'])
app.add_url_rule('/plan/pop', view_func=pop_plan.pop_plan, methods=['POST'])
app.add_url_rule('/task', view_func=create_task.create_task, methods=['POST'])
app.add_url_rule('/task', view_func=list_task.list_task, methods=['GET'])
app.add_url_rule('/task/<id_>', view_func=get_task.get_task, methods=['GET'])
app.add_url_rule('/user/login', view_func=login.login, methods=['POST'])
