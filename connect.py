#asma
from sqlalchemy import create_engine, text

dialect = 'mysql+pymysql'
username = 'root'
password = 'Thi$i$myp4ss'
host = "host.docker.internal"
dbname = 'HOTEL'

chamber_count = 0;
agency_count = 0;
user_count = 0;

engine = create_engine(f"{dialect}://{username}:{password}@{host}/{dbname}")
