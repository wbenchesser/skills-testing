"""
SQL Injection Test Case: SQLAlchemy ORM
CWE-89: SQL Injection
Expected: SAFE (False Positive Test)
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str]

def find_user_by_username(username):
    """
    Find user using SQLAlchemy ORM.
    SAFE: Uses ORM query builder, no raw SQL with user input.
    """
    engine = create_engine('sqlite:///app.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # SAFE: ORM query builder handles parameterization
    user = session.query(User).filter(User.username == username).first()

    session.close()
    return user
