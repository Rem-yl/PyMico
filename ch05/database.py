from pathlib import Path

import yaml
from sqlalchemy.orm import declarative_base


def load_mysql_url(config_file: str) -> str:
    config_path = Path(__file__).parent / config_file

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    mysql_conf = config["mysql"]
    url = (
        f"mysql+pymysql://{mysql_conf['user']}:{mysql_conf['password']}"
        f"@{mysql_conf['host']}:{mysql_conf['port']}/{mysql_conf['database']}"
    )
    return url


DATABASE_URL = load_mysql_url("config.yaml")
Base = declarative_base()
