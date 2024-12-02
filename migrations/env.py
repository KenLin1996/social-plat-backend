import logging
from logging.config import fileConfig

from flask import current_app
import os
from dotenv import load_dotenv
from alembic import context

# 加載 .env 文件
load_dotenv()

# 取得資料庫 URL
database_url = os.getenv('SQLALCHEMY_DATABASE_URI')


# 設定 Alembic 使用從環境變數取得的資料庫 URL
config = context.config
config.set_main_option('sqlalchemy.url', database_url)

# 解析配置文件，設置 logging
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')


def get_engine_url():
    """
    從 Flask 應用配置中讀取 SQLAlchemy URL
    """
    # 直接從 Flask 應用的配置中讀取資料庫 URL
    return current_app.config['SQLALCHEMY_DATABASE_URI']


# 設置 sqlalchemy.url
config.set_main_option('sqlalchemy.url', get_engine_url())
# 目標資料庫元資料
target_db = current_app.extensions['migrate'].db


def get_metadata():
    if hasattr(target_db, 'metadatas'):
        return target_db.metadatas[None]
    return target_db.metadata


def run_migrations_offline():
    """以離線模式運行遷移"""

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=get_metadata(), literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """以線上模式運行遷移"""
    # 這個回調函數防止在沒有變更的情況下生成自動遷移
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    conf_args = current_app.extensions['migrate'].configure_args
    if conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    connectable = current_app.extensions['migrate'].db.engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            **conf_args
        )

        with context.begin_transaction():
            context.run_migrations()


# 根據 Alembic 配置，決定是否進行離線或線上遷移
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
