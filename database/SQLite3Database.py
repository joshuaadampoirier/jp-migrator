import logging 

from database.BaseDatabase import BaseDatabase 

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


class SQLite3Database(BaseDatabase):
    '''
    SQLite3 database class.

    Parameters 
    ----------
    cnxn:       database server connection
                Connection to the database.
    '''
    def __init__(self, cnxn):
        logging.info('Creating database object')
        self.cnxn = cnxn 
        self.__migrations_run()

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
        logging.info('Creating _migrationsrun table')
        
        # open sql file
        f = open('database/sqlite3/_MigrationsRun.sql', 'r')
        cursor = self.cnxn.cursor()

        # run sql command
        sql = f.read() 
        cursor.execute(sql)
        self.cnxn.commit()
        
        # cleanup
        f.close()
        cursor.close()