import logging 
import pkg_resources 

from psycopg2.errors import DuplicateDatabase 
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from database.BaseDatabase import BaseDatabase 

logging.basicConfig(
    filename='PostgreSQLDatabase.log',
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


class PostgreSQLDatabase(BaseDatabase):
    '''
    PostgreSQL database class.

    Parameters 
    ----------
    cnxn:       database server connection
                Connection to the database.

    dbname:     string 
                Name of the database to be created.
    '''
    def __init__(self, cnxn, dbname):
        logging.info('Creating PostgreSQL database object')
        self.cnxn = cnxn 
        self.dbname = dbname
        self.__create_database()
        self.__migrations_run()

    def __create_database(self):
        '''
        Create the database if it does not already exist.

        Parameters
        ----------
        None 

        Returns
        -------
        None 
        '''
        logging.info('Creating PostgreSQL database')

        # localize connection object
        cnxn = self.cnxn 
        cnxn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # build query and open cursor
        sql = 'CREATE DATABASE {db}'.format(db=self.dbname)
        cursor = cnxn.cursor() 

        # create the database if it doesn't exist 
        try:
            cursor.execute(sql)
            cnxn.commit()
        except DuplicateDatabase:
            logging.info('Database already exists')
        
        # cleanup
        cursor.close() 

    def __migrations_run(self):
        '''
        If it does not exist, create a table to track the migrations executed
        against the database.

        Parameters
        ----------
        None 

        Returns
        -------
        None 
        '''
        logging.info('Create _migrationsrun table')
        
        # open sql file
        path = 'postgresql/_MigrationsRun.sql'
        filepath = pkg_resources.resource_filename(__name__, path)
        f = open(filepath, 'r')        

        cursor = self.cnxn.cursor()

        # run sql command
        sql = f.read() 
        cursor.execute(sql)
        self.cnxn.commit()
    
        # cleanup
        f.close()
        cursor.close()