from sqlalchemy import create_engine
conn_string = 'mysql://{user}:{password}@{host}:{port}/{db}?charset=utf8'.format(
    user="Unnamed", 
    password='RyMe/s67Jw4=', 
    host = 'jsedocc7.scrc.nyu.edu', 
    port=3306, 
    db='unnamed',
    encoding = 'utf-8'
)
engine = create_engine(conn_string)
engine.execute('CREATE DATABASE IF NOT EXISTS unnamed')
engine.execute('USE unnamed')

%reload_ext sql_magic
%config SQL.conn_name = 'engine'