import pickle
import sqlite3

from datetime import datetime

from .go import Game

SETUP_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS games (
        id integer PRIMARY KEY,
        p1_name text NOT NULL,
        p2_name text NOT NULL,
        game_started datetime NOT NULL,
        last_move_date datetime NOT NULL,
        game_ended datetime,
        game_result text,
        game_object blob NOT NULL
    );
    """

CREATE_NEW_GAME = """
    INSERT INTO games(p1_name, p2_name, game_started, last_move_date, game_object)
    VALUES(?, ?, ?, ?, ?);
    """

DELETE_GAME = """
    DELETE FROM games WHERE id = ?;
    """


class GameDatabase:
    def __init__(self) -> None:
        self._conn = sqlite3.connect("resources/games.db")
        c = self._conn.cursor()
        c.execute(SETUP_TABLE_SQL)
        c.close()

    @property
    def connection(self) -> sqlite3.Connection:
        return self._conn

    def get_games(self) -> list[tuple]:
        c = self.connection.cursor()
        c.execute("SELECT * FROM games WHERE game_ended is NULL;")
        return c.fetchall()

    def get_all_games(self) -> list[tuple]:
        c = self.connection.cursor()
        c.execute("SELECT * FROM games;")
        return c.fetchall()

    def new_game(self, game: Game) -> int | None:
        time = datetime.now().isoformat(timespec="seconds")
        c = self.connection.cursor()
        params = (game.p1_name, game.p2_name, time, time, pickle.dumps(game))
        c.execute(CREATE_NEW_GAME, params)
        self.connection.commit()
        return c.lastrowid

    def delete_game(self, id: int) -> None:
        c = self.connection.cursor()
        c.execute(DELETE_GAME, (id,))
        self.connection.commit()
