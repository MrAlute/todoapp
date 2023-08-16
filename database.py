from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



# # Construct the SQLAlchemy Database URL
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:aluteceo@localhost/TodoApplicationDatabase"


# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"
# SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:{encoded_password}@127.0.0.1:3306/todoapp"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base = declarative_base()