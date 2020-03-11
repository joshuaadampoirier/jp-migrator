import logging 
import sqlite3 

from server.BaseServer import BaseServer 
from database.SQLite3Database import SQLite3Database 

logging.basicConfig(
    filename='SQLite3Database.log',
    level=logging.INFO,
    format='|' \
    '%(asctime)-18s|' \
    '%(levelname)-4s|' \
    '%(module)-18s|' \
    '%(filename)-18s:%(lineno)-4s|' \
    '%(funcName)-18s|' \
    '%(message)-32s|',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class SQLite3Server(BaseServer):
    '''
    SQLite3 server object.

    SQLite3 databases are actually serverless and have native python 
    connections, so they are easy to work with.

    Parameters 
    ----------
    dbname:     string 
                Name of the database to connect to. 

    cnxn:       database connection object
                Connection to the SQLite3 database.
    '''
    def __init__(self, dbname):
        logging.info('Creating SQLite3 Server')
        self.dbname = dbname 
        self.cnxn = self.__establish_connection()
        self.database = SQLite3Database(self.cnxn)

    def __del__(self):
        logging.info('Closing server connection')
        self.cnxn.close()

    def __establish_connection(self):
        '''
        Retrieve connection to the SQLite3 database server.

        Parameters 
        ----------
        None

        Returns
        -------
        cnxn:       connection object 
                    Open connection to the SQLite3 database server.
        '''
        logging.info('Establishing server connection')
        
        cnxn = sqlite3.connect(
            'Database={database}.db'.format(database=self.dbname)
        )

        return cnxn 