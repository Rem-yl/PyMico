from pathlib import Path

import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


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
engine = create_engine(DATABASE_URL, echo=True)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
