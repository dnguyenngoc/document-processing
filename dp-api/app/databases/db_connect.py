from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from settings import config


engine = create_engine(
    config.SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, echo=True
)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base(metadata=MetaData(schema=config.DATABASE_SCHEMA))


from starlette.requests import Request
def get_db(request: Request):
    return request.state.db


def get_engine():
    return engine