#!/usr/bin/env python3

from sqlalchemy import create_engine, delete, select
from sqlalchemy.orm import sessionmaker

from models import Game, Review, User, game_user

if __name__ == "__main__":
    engine = create_engine("sqlite:///many_to_many.db", echo=True)
    Session = sessionmaker(
        bind=engine,
    )
    session = Session()

    session.execute(delete(Game))
    session.execute(delete(User))
    session.execute(delete(game_user))

    user_1 = User(name="Ben")
    user_2 = User(name="Prabhdip")
    session.add_all([user_1, user_2])
    session.commit()

    game = Game(title="Super Marvin 128")
    game.users.append(user_1)
    game.users.append(user_2)
    session.add(game)
    session.commit()

    import ipdb

    ipdb.set_trace()
