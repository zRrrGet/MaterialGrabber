from dataclasses import dataclass

from environs import Env


@dataclass
class Config:
    token: str
    admin_ids: list[int]
    db_url: str
    mega_path: str


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        token=env.str('BOT_TOKEN'),
        admin_ids=list(map(int, env.list('ADMINS'))),
        db_url=env.str('DB_URL'),
        mega_path=env.str('MEGA_PATH')
    )
