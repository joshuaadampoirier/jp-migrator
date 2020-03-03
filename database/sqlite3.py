from database.base import BaseDatabase 


class SQLite3Database(BaseDatabase):
    '''
    SQLite3 database class.

    Parameters 
    ----------
    cnxn:       database server connection
                Connection to the database.
    '''
    def __init__(self, cnxn):
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