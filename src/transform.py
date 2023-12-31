import hashlib
from dataclasses import dataclass
from io import StringIO
from typing import Any, Optional

import chess
import chess.pgn
from chess.pgn import Game

from src.utils.config import Config
from src.utils.logger import Logger


@dataclass
class TransformUserData:
    log: Logger
    config: Config

    def create_gcs_dict_object(self, game_num: int, game_pgn: dict) -> tuple[Any, Any]:
        game = self.read_chess_game_from_string(game_pgn)
        headers = dict(game.headers)  # type: ignore

        game_id = self.generate_unique_id(
            self.config.username, headers["UTCDate"], headers["UTCTime"]
        )
        game_data = {
            "game_id": game_id,
            "username": self.config.username,
            "depth": self.config.depth,
            "pgn": game_pgn["pgn"],
            "game_num": game_num,
            "headers": headers,
        }

        file_name = f"{game_id}.json"
        return (game_data, file_name)

    def read_chess_game_from_string(self, game_pgn: dict) -> Optional[Game]:
        pgn = StringIO(game_pgn["pgn"])
        return chess.pgn.read_game(pgn)

    @staticmethod
    def generate_unique_id(username: str, game_date: str, game_time: str) -> str:
        base_id = f"{username}_{game_date}_{game_time}"
        hash_id = hashlib.sha1(base_id.encode())

        return str(hash_id.hexdigest())
