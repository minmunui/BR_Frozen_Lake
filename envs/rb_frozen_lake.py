import numpy as np
from gymnasium.vector.utils import spaces

from envs.frozen_lake import FrozenLakeEnv
from utils.utils import is_valid


class RBFrozenLakeEnv(FrozenLakeEnv):
    def __init__(self, **kwargs):
        super(RBFrozenLakeEnv, self).__init__(**kwargs)
        self.observation_space = spaces.Dict({
            "map": self.observation_space["map"],
            "current": self.observation_space["current"],
        })

    def observe(self):
        return {
            "map": self.grid,
            "current": self.current
        }

    def generate_random_map(self):
        valid = False
        _map = []
        while not valid:
            _map = np.random.choice([b"F", b"H"], (self.n_row, self.n_col), p=[self.frozen_prob, 1 - self.frozen_prob])
            start = (0, 0)
            _map[start] = b"S"
            valid = find_RB(_map.tolist(), (0, 0))

        _map[valid] = b"G"
        return _map.tolist()


def find_RB(_map, start):
    n_row, n_col = len(_map), len(_map[0])
    last_column = [(i, n_col - 1) for i in range(n_row)][::-1]
    for last_col_cell in last_column:
        if _map[last_col_cell[0]][last_col_cell[1]] == b"H":
            continue
        if is_valid(_map, last_col_cell, start):
            return last_col_cell
    return None
