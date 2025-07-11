from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import yaml

with open ("./config/storage_config.yml", "r") as f:
    variables = yaml.safe_load(f.read())
db_user = variables["database"]["user"]
db_pwd = variables["database"]["password"]
db_hn = variables["database"]["hostname"]
db_port = variables["database"]["port"]
db_name = variables["database"]["db_name"]
engine_url = f"//{db_user}:{db_pwd}@{db_hn}:{db_port}/{db_name}"

engine = create_engine(f"mysql+pymysql:{engine_url}")

def make_session():
    return sessionmaker(bind=engine)()