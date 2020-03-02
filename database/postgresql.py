from database.base import BaseDatabase 


class PostgreSQLDatabase(BaseDatabase):
    '''
    PostgreSQL database class.

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
        f = open('database/postgresql/_MigrationsRun.sql', 'r')
        cursor = self.cnxn.cursor()

        # run sql command
        sql = f.read() 
        cursor.execute(sql)
        
        # cleanup
        f.close()
        cursor.close()