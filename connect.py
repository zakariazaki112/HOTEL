
from sqlalchemy import create_engine, text

dialect = 'mysql'
username = 'root'
password = 'Thi$i$myp4ss'
host = "127.0.0.1"
dbname = 'HOTEL'

chamber_count = 0;
agency_count = 0;
user_count = 0;

engine = create_engine(f"{dialect}://{username}:{password}@{host}/{dbname}")