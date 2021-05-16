# -*- coding: utf8 -*-
# 为历史用户补充anywhere的location记录
import os

import click

from nest.app.entity.location import Location
from nest.infra.config import Config
from nest.infra.db_connection import DBUtilsConnectionPool
from nest.infra.repository import RepositoryFactory


@click.command()
def create_location():
    """为历史用户补充地点，并设置历史计划的地点ID。"""
    current_dir = os.path.dirname(__file__)
    config_dir = os.path.join(current_dir, '../config')
    file_name = 'default'
    mode = os.environ.get('MODE')
    if mode == 'unittest':
        file_name = 'unittest'
    config_file = os.path.join(config_dir, file_name + '.ini')
    config = Config(config_file)
    mysql_connection = DBUtilsConnectionPool(config)
    repository_factory = RepositoryFactory(mysql_connection)
    location_repository = repository_factory.location()
    plan_repository = repository_factory.plan()
    user_repository = repository_factory.user()
    page = 1
    per_page = 100
    while True:
        click.echo('获取第{}页用户数据'.format(page))
        users = user_repository.find(
            page=page,
            per_page=per_page,
        )
        if len(users) == 0:
            break
        for user in users:
            default_location = location_repository.get_default(user_id=user.id)
            if default_location is not None:
                continue
            location = Location.new(name='anywhere', user_id=user.id)
            location_repository.add(location=location)
            click.echo('为用户{}创建了默认地点'.format(user.id))
            # 同时还要修改该用户所有的历史计划
            page2 = 1
            per_page2 = 100
            while True:
                click.echo('获取用户{}第{}页的计划数据'.format(user.id, page2))
                plans = plan_repository.find_as_queue(
                    page=page2,
                    per_page=per_page2,
                    user_id=user.id,
                )
                if len(plans) == 0:
                    break
                for plan in plans:
                    if plan.location_id is not None:
                        continue
                    plan.location_id = location.id
                    plan_repository.add(plan)
                page2 += 1
        page += 1


if __name__ == '__main__':
    create_location()
