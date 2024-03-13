import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from model import create_tables, drop_tables, insert_table, get_shops
from dotenv import load_dotenv

load_dotenv()
connection_driver = os.getenv('connection_driver')
username = os.getenv('user')
password = os.getenv('password')
server_name = os.getenv('server_name')
port = os.getenv('port')
db_name = os.getenv('db_name')

DSN = f'{connection_driver}://{username}:{password}@{server_name}:{port}/{db_name}'
#print(DSN)
engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()

#удаления создания таблиц
drop_tables(session, engine)
create_tables(session, engine)

#заполнения таблиц
BASE_DIR = os.getcwd()
FOLDER_NAME = 'fixtures'
FILE_NAME = 'tests_data.json'
full_path = os.path.join(BASE_DIR, FOLDER_NAME, FILE_NAME)
insert_table(session, full_path)

# поиск по издателю
get_shops(session)

session.close()