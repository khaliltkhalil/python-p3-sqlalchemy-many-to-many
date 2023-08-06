from sqlalchemy import create_engine, func, event
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import Engine
import sqlite3

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if type(dbapi_connection) is sqlite3.Connection:  # play well with other DB backends
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


game_user = Table(
    "game_users",
    Base.metadata,
    Column("game_id", ForeignKey("games.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    extend_existing=True,
)


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer(), primary_key=True)
    title = Column(String())
    genre = Column(String())
    platform = Column(String())
    price = Column(Integer())

    reviews = relationship("Review", backref=backref("game"))

    users = relationship("User", secondary=game_user, back_populates="games")

    def __repr__(self):
        return (
            f"Game(id={self.id}, "
            + f"title={self.title}, "
            + f"platform={self.platform})"
        )


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer(), primary_key=True)
    score = Column(Integer())
    comment = Column(String())

    game_id = Column(Integer(), ForeignKey("games.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    def __repr__(self):
        return (
            f"Review(id={self.id}, "
            + f"score={self.score}, "
            + f"game_id={self.game_id})"
        )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    reviews = relationship("Review", backref=backref("user"))
    games = relationship("Game", secondary=game_user, back_populates="users")

    def __repr__(self):
        return f"User(id={self.id}, " + f"name={self.name})"
