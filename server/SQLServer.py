import logging 
import pymssql 

from pymssql import OperationalError

from server.BaseServer import BaseServer 
from database.SQLServerDatabase import SQLServerDatabase 


logging.basicConfig(
    filename='SQLServerDatabase.log',
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


class SQLServer(BaseServer):
    '''
    SQLServer server object.

    Parameters 
    ----------
    server:     string 
                Server address to connect to.

    port:       int
                Port to connect to server through
    
    user:       string 
                Database server login name.

    password:   string 
                Database server login password.

    dbname:     string 
                Name of the database to connect to. 
                Defaults to master, the system database.

    cnxn:       Database connection object
                Connection to the SQL Server database.
    '''
    def __init__(
        self, 
        server,
        port,
        user, 
        password, 
        dbname='master',
    ):
        logging.info('Creating SQL Server server object')

        self.server = server
        self.port = port 
        self.user = user  
        self.password = password 
        self.dbname = dbname 

        self.cnxn = self.__establish_connection()
        self.database = SQLServerDatabase(self.cnxn, dbname)

    def __del__(self):
        try:
            logging.info('Closing database connection')
            self.cnxn.close()
        except AttributeError:
            logging.warning('Unable to close connection')

    def __establish_connection(self):
        '''
        Retrieve connection to the SQL Server database server.

        Parameters 
        ----------
        None

        Returns
        -------
        cnxn:       connection object 
                    Open connection to the SQL Server database server.
        '''
        logging.info('Establishing server connection')
        
        try:
            cnxn = pymssql.connect(
                server=self.server,
                port=self.port,
                user=self.user, 
                password=self.password,
                database=self.dbname
            )

        except OperationalError:
            logging.warning('Unable to connect, trying system database ...')

            base_cnxn = pymssql.connect(
                server=self.server,
                port=self.port, 
                user=self.user,
                password=self.password,
                database='master'
            )

            logging.info('Connection to system database established, creating database')
            
            # attempt to create database 
            database = SQLServerDatabase(base_cnxn, self.dbname)
            base_cnxn.close()

            # second/final attempt to connect to database (now that db is there)
            cnxn = pymssql.connect(
                server=self.server,
                port=self.port,
                user=self.user, 
                password=self.password,
                database=self.dbname
            )

        return cnxn 