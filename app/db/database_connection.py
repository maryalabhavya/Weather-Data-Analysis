import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import sqlalchemy.ext.declarative as _declarative


# Set up the database engine and session
_SQLALCHEMY_DATABASE = 'sqlite:///weather_data.db'
engine = _sql.create_engine(_SQLALCHEMY_DATABASE)
SessionLocal = _orm.sessionmaker(autoflush=False, bind=engine)
session = SessionLocal()
Base = _declarative.declarative_base()


# Create the database tables if they don't exist
def create_database():
    return Base.metadata.create_all(bind=engine)


def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()


