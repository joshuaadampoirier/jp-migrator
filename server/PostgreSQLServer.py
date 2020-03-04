import psycopg2

from psycopg2 import OperationalError 
from psycopg2.errors import DuplicateDatabase 
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from server.BaseServer import BaseServer 
from database.PostgreSQLDatabase import PostgreSQLDatabase 


class PostgreSQLServer(BaseServer):
    '''
    PostgreSQL server object.

    Parameters 
    ----------
    user:       string 
                Database server login name.

    password:   string 
                Database server login password.

    host:       string 
                Host server address.

    port:       string 
                Port host server is serving through.

    dbname:     string 
                Name of the database to connect to. 
                Defaults to postgres, the system database.

    cnxn:       Database connection object
                Connection to the PostgreSQL database.
    '''
    def __init__(
        self, 
        user, 
        password, 
        host='localhost', 
        port='5432', 
        dbname='postgres'
    ):
        self.user = user 
        self.password = password 
        self.host = host 
        self.port = port 
        self.dbname = dbname 
        self.cnxn = self.__establish_connection()
        self.database = PostgreSQLDatabase(self.cnxn, dbname)

    def __del__(self):
        try:
            self.cnxn.close()
        except AttributeError:
            print('Warning: Unable to close server connection.')

    def __establish_connection(self):
        '''
        Retrieve connection to the PostgreSQL database server.

        Parameters 
        ----------
        None 

        Returns
        -------
        cnxn:       connection object 
                    Open connection to the PostgreSQL database server.
        '''
        try:
            cnxn = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.dbname
            )
        except OperationalError:
            # attempt to create database by connecting to system database
            base_cnxn = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database='postgres'
            ) 

            # attempt to create database 
            database = PostgreSQLDatabase(base_cnxn, self.dbname)
            base_cnxn.close()

            # second/final attempt to connect to database (now that db is there)
            cnxn = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.dbname
            )

        cnxn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
        return cnxn 