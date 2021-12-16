import sys
sys.path = ['', '../../'] + sys.path[1:]
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# DB models
from databases.models import user
from databases.db_connect import Base
from settings import config as environment


config = context.config
config.set_main_option("sqlalchemy.url", environment.SQLALCHEMY_DATABASE_URL)

fileConfig(config.config_file_name)

# Exceute db models
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        """
        Configure migration context
        1. Pass our models metadata
        2. Set schema for alembic_version table
        3. Load all available schemas
        """
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema=target_metadata.schema,
            include_schemas=True
        )

        with context.begin_transaction():
            """
            By default search_path is setted to "$user",public 
            that why alembic can't create foreign keys correctly
            """
            context.execute('SET search_path TO public')
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()